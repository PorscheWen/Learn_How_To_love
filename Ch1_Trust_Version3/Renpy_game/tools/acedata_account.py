# -*- coding: utf-8 -*-
"""AceData 帳戶：每次呼叫都印剩餘積分與使用期限。

需要 `ACEDATA_PLATFORM_TOKEN`（控制台「平台令牌」，與 API Token 不同）。
"""

from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
TZ8 = timezone(timedelta(hours=8))
USD_PER_CREDIT = 0.095215


def load_env_value(key: str) -> str:
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


def _fmt_expiry(iso) -> str:
    if not iso:
        return "無到期日"
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00")).astimezone(TZ8)
    except ValueError:
        return str(iso)
    now = datetime.now(TZ8)
    days = (dt.date() - now.date()).days
    if days > 0:
        extra = f"（剩 {days} 天）"
    elif days == 0:
        extra = "（今天到期）"
    else:
        extra = f"（已過期 {abs(days)} 天）"
    return dt.strftime("%Y-%m-%d %H:%M") + extra


def _app_name(app: dict) -> str:
    svc = app.get("service") or {}
    return (
        svc.get("title")
        or svc.get("alias")
        or ("全域餘額" if app.get("scope") == "Global" else None)
        or app.get("scope")
        or "未命名服務"
    )


def _soonest_expiry(app: dict):
    dates = []
    if app.get("expired_at"):
        dates.append(app["expired_at"])
    for cred in app.get("credentials") or []:
        if isinstance(cred, dict) and cred.get("expired_at"):
            dates.append(cred["expired_at"])
    if not dates:
        return None
    return min(dates)


def report_account(when: str = "") -> None:
    """印出各服務剩餘積分與期限。查詢失敗不拋錯。"""
    platform_token = load_env_value("ACEDATA_PLATFORM_TOKEN")
    tag = f"[AceData{(' ' + when) if when else ''}]"
    if not platform_token:
        print(f"{tag} 未設定 ACEDATA_PLATFORM_TOKEN，無法查餘額／期限"
              "（到 platform.acedata.cloud 控制台建立平台令牌後寫入 tools\\.env）")
        return
    req = urllib.request.Request(
        "https://platform.acedata.cloud/api/v1/applications/?user_id=me&limit=100",
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {platform_token}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"{tag} 查詢失敗（不影響本次生成）：{e}")
        return

    items = data.get("items") or data.get("results") or []
    total_rem = 0.0
    total_used = 0.0
    for app in items:
        rem = app.get("remaining_amount")
        used = app.get("used_amount")
        if isinstance(rem, (int, float)):
            total_rem += rem
        else:
            rem = 0
        if isinstance(used, (int, float)):
            total_used += used
        else:
            used = 0
        name = _app_name(app)
        expiry = _fmt_expiry(_soonest_expiry(app))
        print(
            f"{tag} {name}  剩餘 {float(rem):.2f} / 已用 {float(used):.2f} Credits  "
            f"期限：{expiry}"
        )
    print(
        f"{tag} 合計剩餘 {total_rem:.2f} Credits（約 ${total_rem * USD_PER_CREDIT:.2f} USD）"
        f"  已用 {total_used:.2f}"
    )


report_balance = report_account


if __name__ == "__main__":
    report_account()
