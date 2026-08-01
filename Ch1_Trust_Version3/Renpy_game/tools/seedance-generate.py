# -*- coding: utf-8 -*-
r"""Seedance 圖生影片工具（AceData Cloud API）

用法範例（PowerShell，在 Renpy_game 目錄下）：

  # 首幀模式：從這張圖開始動（構圖與原圖一致，適合抽幀做序列動畫）
  python tools\seedance-generate.py --image game\images\dog\dog-sit.png `
      --prompt "小狗開心地搖尾巴，身體姿勢保持坐姿，背景乾淨" --duration 5

  # 角色參考模式：保留角色外觀，場景動作由 prompt 決定（僅 Seedance 2.0）
  python tools\seedance-generate.py --image game\images\dog\dog-sit.png --role reference `
      --prompt "同一隻小狗在草地上奔跑" --duration 5

Token 讀取順序：
  1. 環境變數 ACEDATA_API_TOKEN
  2. tools\.env 內的 ACEDATA_API_TOKEN=...（此檔已被 .gitignore 排除，勿提交）
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

API_URL = "https://api.acedata.cloud/seedance/videos"
DEFAULT_MODEL = "doubao-seedance-2-0-fast-260128"  # 2.0 fast：最便宜，最高 720p
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_env_value(key):
    val = os.environ.get(key, "").strip()
    if val:
        return val
    env_path = os.path.join(TOOLS_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(key + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def load_token():
    return load_env_value("ACEDATA_API_TOKEN")


def report_balance():
    """查詢並顯示剩餘積分。需要平台 Token（ACEDATA_PLATFORM_TOKEN，
    與 API Token 不同，於控制台「平台令牌」頁建立）。查不到時靜默略過。"""
    platform_token = load_env_value("ACEDATA_PLATFORM_TOKEN")
    if not platform_token:
        print("[餘額] 未設定 ACEDATA_PLATFORM_TOKEN，無法查詢剩餘積分"
              "（到 platform.acedata.cloud 控制台建立平台令牌後寫入 tools\\.env）")
        return
    req = urllib.request.Request(
        "https://platform.acedata.cloud/api/v1/applications/?user_id=me&limit=100",
        headers={"accept": "application/json",
                 "authorization": f"Bearer {platform_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # 查餘額失敗不影響主流程
        print(f"[餘額] 查詢失敗（不影響生成結果）：{e}")
        return
    items = data.get("items") or data.get("results") or []
    total = 0.0
    for app in items:
        amt = app.get("remaining_amount")
        if isinstance(amt, (int, float)):
            total += amt
    print(f"[餘額] 剩餘積分：{total:.2f} Credits（約 ${total * 0.095215:.2f} USD）")


def image_to_data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def pad_to_ratio(path, ratio_str, margin):
    """把圖片置中墊到指定比例的白色畫布上（四周留 margin 比例的白邊），
    避免模型為了湊輸出比例而裁切主體。回傳 base64 data URL。"""
    from PIL import Image  # 延遲載入，未用 --pad 時不需要 Pillow

    rw, rh = (int(x) for x in ratio_str.split(":"))
    img = Image.open(path).convert("RGBA")
    w, h = img.size

    # 主體可用區域 = 畫布的 (1 - 2*margin)，取讓圖片完整放入的最小畫布
    usable = 1.0 - 2.0 * margin
    canvas_w = max(int(w / usable), int(h / usable * rw / rh))
    canvas_h = int(canvas_w * rh / rw)

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))
    canvas.paste(img, ((canvas_w - w) // 2, (canvas_h - h) // 2), img)

    import io
    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_image_item(image, role, pad_ratio=None, pad_margin=0.1):
    """image 可為本地路徑或 http(s) URL。API 要求 image_url 必須是物件格式。"""
    if image.startswith("http://") or image.startswith("https://"):
        url = image
    else:
        if not os.path.exists(image):
            sys.exit(f"[錯誤] 找不到圖片：{image}")
        if pad_ratio:
            url = pad_to_ratio(image, pad_ratio, pad_margin)
        else:
            url = image_to_data_url(image)
    item = {"type": "image_url", "image_url": {"url": url}}
    if role:
        item["role"] = role
    return item


def post_json(url, payload, token, timeout):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"[錯誤] HTTP {e.code}：{body}")
    except urllib.error.URLError as e:
        sys.exit(f"[錯誤] 連線失敗：{e.reason}")


def download(url, out_path, token=None):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=300) as resp, open(out_path, "wb") as f:
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            f.write(chunk)


def main():
    p = argparse.ArgumentParser(description="Seedance 圖生影片（AceData API）")
    p.add_argument("--prompt", required=True, help="動作描述（可用中文）")
    p.add_argument("--image", help="輸入圖片：本地路徑或 URL")
    p.add_argument("--role", choices=["first", "reference", "last"], default="first",
                   help="圖片用途：first=首幀（預設，構圖一致）；reference=角色參考（2.0 限定）；last=尾幀")
    p.add_argument("--last-frame", dest="last_frame", help="尾幀圖片（做循環動畫時與 --image 用同一張）")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"模型 ID（預設 {DEFAULT_MODEL}；標準版 doubao-seedance-2-0-260128 支援 1080p/4k）")
    p.add_argument("--duration", type=int, default=5, help="秒數，2.0 系列 4~15（預設 5）")
    p.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p", "4k"])
    p.add_argument("--ratio", default="adaptive",
                   choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
                   help="寬高比（預設 adaptive 跟隨輸入圖）")
    p.add_argument("--seed", type=int, default=-1, help="隨機種子，固定可重現（預設 -1 隨機）")
    p.add_argument("--moving-camera", action="store_true", help="允許鏡頭移動（預設固定鏡頭，利於抽幀）")
    p.add_argument("--pad", action="store_true",
                   help="先把輸入圖墊到 --ratio 比例的白色畫布再送出，避免主體被裁切（需指定非 adaptive 的 ratio）")
    p.add_argument("--pad-margin", type=float, default=0.1,
                   help="--pad 時四周白邊佔畫布的比例（預設 0.1）")
    p.add_argument("--out", help="輸出 mp4 路徑（預設 tools/output/seedance/<時間戳>.mp4）")
    args = p.parse_args()

    if args.pad and args.ratio == "adaptive":
        sys.exit("[錯誤] --pad 需要明確的 --ratio（例如 1:1 或 3:4），不能用 adaptive")

    token = load_token()
    if not token:
        sys.exit("[錯誤] 未設定 ACEDATA_API_TOKEN。請設環境變數，或在 tools\\.env 寫入：\n"
                 "  ACEDATA_API_TOKEN=你的token")

    role_map = {"first": "first_frame", "reference": "reference_image", "last": "last_frame"}
    pad_ratio = args.ratio if args.pad else None
    content = [{"type": "text", "text": args.prompt}]
    if args.image:
        # 只有單張圖且未指定尾幀時，first_frame 不需要 role 欄位也可，但明確標注較穩
        content.append(build_image_item(args.image, role_map[args.role], pad_ratio, args.pad_margin))
    if args.last_frame:
        if args.role == "reference":
            sys.exit("[錯誤] reference_image 不能與 first/last_frame 併用（API 限制）")
        content.append(build_image_item(args.last_frame, "last_frame", pad_ratio, args.pad_margin))

    payload = {
        "model": args.model,
        "content": content,
        "duration": args.duration,
        "resolution": args.resolution,
        "ratio": args.ratio,
        "seed": args.seed,
        "watermark": False,
    }
    # fast 模型（i2v／flf2v）不接受 camerafixed，須留空；鏡頭固定改由 prompt 描述
    if not args.last_frame and "fast" not in args.model:
        payload["camerafixed"] = not args.moving_camera

    print(f"[送出] model={args.model} duration={args.duration}s resolution={args.resolution}")
    print("[等待] 生成約需 1~2 分鐘，請稍候…")
    t0 = time.time()
    result = post_json(API_URL, payload, token, timeout=600)

    if not result.get("success"):
        sys.exit(f"[錯誤] 生成失敗：{json.dumps(result, ensure_ascii=False)}")

    data = result.get("data", {})
    video_url = data.get("video_url")
    if not video_url:
        sys.exit(f"[錯誤] 回應中沒有 video_url：{json.dumps(result, ensure_ascii=False)}")

    out_path = args.out
    if not out_path:
        out_dir = os.path.join(TOOLS_DIR, "output", "seedance")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, time.strftime("%Y%m%d-%H%M%S") + ".mp4")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)

    print(f"[下載] {video_url}")
    download(video_url, out_path)
    elapsed = time.time() - t0
    print(f"[完成] {out_path}（耗時 {elapsed:.0f} 秒）")
    print("[提醒] 影片連結 24 小時後失效，檔案已下載到本地。")
    report_balance()


if __name__ == "__main__":
    main()
