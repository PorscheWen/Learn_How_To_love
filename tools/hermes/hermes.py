#!/usr/bin/env python3
"""
Hermes — LHTL 編排器
  code     : Cursor SDK 寫碼
  test     : 跑 Node 驗證腳本（cron 常用）
  pipeline : SDK 寫碼 → 測試 → 失敗可重試
  agent    : 官方 Hermes CLI（Nous Portal 生圖／TTS）
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JOBS_PATH = ROOT / "jobs.json"


@dataclass
class Config:
    api_key: str
    game_cwd: Path
    model: str
    max_retries: int


def load_config(*, require_api_key: bool = True) -> Config:
    api_key = os.environ.get("CURSOR_API_KEY", "").strip()
    if require_api_key and not api_key:
        sys.exit(
            "缺少 CURSOR_API_KEY。金鑰設定見 Ch1_Trust/Nous_Portal.md，"
            "值寫入 tools/hermes/.env。"
        )

    game_cwd = Path(
        os.environ.get("HERMES_GAME_CWD", ROOT / "../../Ch1_Trust/game")
    ).resolve()
    if not game_cwd.is_dir():
        sys.exit(f"HERMES_GAME_CWD 不存在: {game_cwd}")

    return Config(
        api_key=api_key,
        game_cwd=game_cwd,
        model=os.environ.get("HERMES_MODEL", "composer-2.5"),
        max_retries=int(os.environ.get("HERMES_MAX_RETRIES", "2")),
    )


def load_jobs() -> dict:
    with JOBS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def run_sdk_prompt(cfg: Config, prompt: str, extra_context: str = "") -> int:
    """Cursor SDK 寫碼。回傳 process exit code（0=成功）。"""
    try:
        from cursor_sdk import Agent, AgentOptions, CursorAgentError, LocalAgentOptions
    except ImportError:
        sys.exit("請先安裝: pip install -r requirements.txt")

    full_prompt = prompt
    if extra_context:
        full_prompt = f"{prompt}\n\n---\n上一輪測試輸出（請依此修復）:\n```\n{extra_context}\n```"

    print(f"[hermes] SDK prompt → cwd={cfg.game_cwd}")
    print(f"[hermes] model={cfg.model}")

    try:
        result = Agent.prompt(
            full_prompt,
            AgentOptions(
                api_key=cfg.api_key,
                model=cfg.model,
                local=LocalAgentOptions(cwd=str(cfg.game_cwd)),
            ),
        )
    except CursorAgentError as err:
        print(f"[hermes] SDK 啟動失敗: {err.message} (retryable={err.is_retryable})", file=sys.stderr)
        return 1

    print(f"[hermes] run status={result.status}")
    if result.result:
        print(result.result[:4000])
    if result.status == "error":
        return 2
    return 0 if result.status == "finished" else 1


def run_tests(cfg: Config, test_scripts: list[str]) -> tuple[int, str]:
    """在 game cwd 執行 node 驗證腳本。回傳 (exit_code, combined_output)。"""
    if not test_scripts:
        return 0, ""

    outputs: list[str] = []
    worst = 0

    for rel in test_scripts:
        script = (cfg.game_cwd / rel).resolve()
        if not script.is_file():
            msg = f"找不到測試腳本: {script}"
            print(f"[hermes] {msg}", file=sys.stderr)
            outputs.append(msg)
            worst = max(worst, 1)
            continue

        print(f"[hermes] test → node {rel}")
        proc = subprocess.run(
            ["node", str(script)],
            cwd=str(cfg.game_cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        block = f"=== {rel} (exit {proc.returncode}) ===\n{proc.stdout}{proc.stderr}"
        outputs.append(block)
        if proc.returncode != 0:
            worst = proc.returncode
            print(block, file=sys.stderr)
        else:
            print(f"[hermes] OK: {rel}")

    return worst, "\n\n".join(outputs)


def cmd_code(cfg: Config, prompt: str) -> int:
    return run_sdk_prompt(cfg, prompt)


def cmd_test(cfg: Config, tests: list[str] | None) -> int:
    jobs = load_jobs()
    scripts = tests or jobs.get("defaultTests", [])
    code, _ = run_tests(cfg, scripts)
    return code


def resolve_hermes_cli() -> Path:
    """官方 Hermes Agent CLI（含 image_generate / text_to_speech）。"""
    env = os.environ.get("HERMES_CLI_PATH", "").strip()
    if env:
        path = Path(env).expanduser()
        if path.is_file():
            return path.resolve()
        sys.exit(f"HERMES_CLI_PATH 不存在: {path}")

    localappdata = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        Path(localappdata) / "hermes" / "hermes-agent" / "venv" / "Scripts" / "hermes.exe",
        Path.home() / ".local" / "bin" / "hermes",
        Path("/usr/local/bin/hermes"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    found = shutil.which("hermes")
    if found:
        return Path(found).resolve()

    sys.exit(
        "找不到官方 Hermes CLI。請安裝 hermes-agent 或於 .env 設定 HERMES_CLI_PATH。"
    )


def run_official_agent(
    prompt: str,
    *,
    toolsets: list[str],
    skills: list[str] | None = None,
    yolo: bool = True,
) -> int:
    cli = resolve_hermes_cli()
    model = os.environ.get("HERMES_AGENT_MODEL", "google/gemini-2.5-pro")
    provider = os.environ.get("HERMES_AGENT_PROVIDER", "nous")
    cwd = Path(
        os.environ.get("HERMES_AGENT_CWD", ROOT / "../..")
    ).resolve()

    cmd = [
        str(cli),
        "-z",
        prompt,
        "-t",
        ",".join(toolsets),
        "-m",
        model,
        "--provider",
        provider,
    ]
    if skills:
        cmd.extend(["--skills", ",".join(skills)])
    if yolo:
        cmd.append("--yolo")

    print(f"[hermes] official agent → {cli}")
    print(f"[hermes] cwd={cwd}")
    print(f"[hermes] toolsets={toolsets} model={provider}/{model}")

    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        print(f"[hermes] agent 失敗 exit={proc.returncode}", file=sys.stderr)
    return proc.returncode


def cmd_agent(job_name: str, prompt: str | None) -> int:
    jobs = load_jobs()
    job = jobs.get("jobs", {}).get(job_name)
    if not job:
        sys.exit(f"找不到 job: {job_name}")

    if job.get("kind") != "agent":
        sys.exit(f"job {job_name} 不是 agent 類型（kind: agent）")

    final_prompt = prompt or job.get("prompt")
    if not final_prompt:
        sys.exit("agent job 需要 prompt")

    toolsets = job.get("toolsets") or []
    if not toolsets:
        sys.exit(f"job {job_name} 缺少 toolsets")

    skills = job.get("skills") or []
    yolo = bool(job.get("yolo", True))
    return run_official_agent(
        final_prompt,
        toolsets=toolsets,
        skills=skills,
        yolo=yolo,
    )


def cmd_pipeline(cfg: Config, job_name: str | None, prompt: str | None, tests: list[str] | None) -> int:
    jobs = load_jobs()
    job = jobs.get("jobs", {}).get(job_name, {}) if job_name else {}

    if job_name and job.get("kind") == "agent":
        return cmd_agent(job_name, prompt)

    final_prompt = prompt or job.get("prompt")
    final_tests = tests or job.get("tests") or jobs.get("defaultTests", [])

    if not final_prompt and not final_tests:
        sys.exit("pipeline 需要 --job、--prompt 或 --test")

    test_output = ""

    if final_prompt:
        for attempt in range(cfg.max_retries + 1):
            print(f"[hermes] pipeline 寫碼 attempt {attempt + 1}/{cfg.max_retries + 1}")
            code = run_sdk_prompt(cfg, final_prompt, extra_context=test_output if attempt else "")
            if code != 0:
                return code

            if not final_tests:
                return 0

            test_code, test_output = run_tests(cfg, final_tests)
            if test_code == 0:
                print("[hermes] pipeline 完成：寫碼 + 測試皆通過")
                return 0

            if attempt >= cfg.max_retries:
                print("[hermes] pipeline 失敗：測試未通過且已用盡重試", file=sys.stderr)
                return test_code

            print("[hermes] 測試失敗，帶錯誤輸出重試 SDK…")
    else:
        test_code, _ = run_tests(cfg, final_tests)
        return test_code

    return 1


def cmd_setup_portal(*, open_browser: bool = False, install_deps: bool = False) -> int:
    """初始化 Nous Portal 並啟動 HTTP 服務。"""
    env_path = ROOT / ".env"
    example = ROOT / ".env.example"
    if not env_path.is_file() and example.is_file():
        env_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[hermes] 已建立 {env_path.name}（金鑰見 Ch1_Trust/Nous_Portal.md）")

    if install_deps:
        print("[hermes] pip install -r requirements.txt …")
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
            cwd=str(ROOT),
            check=False,
        )
        if proc.returncode != 0:
            return proc.returncode

    portal_script = ROOT / "portal_server.py"
    if not portal_script.is_file():
        sys.exit(f"缺少 {portal_script}")

    _load_dotenv_file()
    port = os.environ.get("HERMES_PORTAL_PORT", "8780")
    host = os.environ.get("HERMES_PORTAL_HOST", "127.0.0.1")
    url = f"http://{host}:{port}/"

    print(f"[hermes] 啟動 Nous Portal → {url}")
    if open_browser:
        if sys.platform == "win32":
            subprocess.Popen(["powershell", "-NoProfile", "-Command", f'Start-Process "{url}"'])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])

    os.execv(sys.executable, [sys.executable, str(portal_script)])


def _load_dotenv_file() -> None:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Hermes 編排：Cursor SDK 寫碼 + 測試")
    sub = parser.add_subparsers(dest="command", required=True)

    p_code = sub.add_parser("code", help="僅 Cursor SDK 寫碼")
    p_code.add_argument("prompt", help="給 Agent 的指令")

    p_test = sub.add_parser("test", help="僅跑驗證腳本（cron 用）")
    p_test.add_argument("--scripts", nargs="*", help="相對 game cwd 的腳本路徑")

    p_pipe = sub.add_parser("pipeline", help="寫碼 → 測試 → 失敗重試")
    p_pipe.add_argument("--job", help="jobs.json 中的 job 名稱")
    p_pipe.add_argument("--prompt", help="覆寫 job 的 prompt")
    p_pipe.add_argument("--test", nargs="*", dest="tests", help="覆寫測試腳本列表")

    p_agent = sub.add_parser("agent", help="官方 Hermes（Nous Portal 生圖／TTS）")
    p_agent.add_argument("--job", required=True, help="jobs.json 中的 agent job")
    p_agent.add_argument("--prompt", help="覆寫 job 的 prompt")

    sub.add_parser("list", help="列出 jobs.json 中的 job")

    p_setup = sub.add_parser("setup", help="初始化 Hermes / Nous Portal")
    p_setup.add_argument("--portal", action="store_true", help="啟動 Nous Portal 門戶")
    p_setup.add_argument("--no-browser", action="store_true", help="不自動開啟瀏覽器")
    p_setup.add_argument("--install", action="store_true", help="pip install requirements.txt")

    args = parser.parse_args()

    if args.command == "setup":
        if not args.portal:
            sys.exit("用法: hermes setup --portal")
        sys.exit(cmd_setup_portal(open_browser=not args.no_browser, install_deps=args.install))

    if args.command == "list":
        data = load_jobs()
        for name, job in data.get("jobs", {}).items():
            kind = job.get("kind", "pipeline")
            print(f"{name} [{kind}]: {job.get('description', '')}")
        return

    if args.command == "agent":
        _load_dotenv_file()
        sys.exit(cmd_agent(args.job, args.prompt))

    if args.command == "test":
        cfg = load_config(require_api_key=False)
        sys.exit(cmd_test(cfg, args.scripts))

    if args.command == "pipeline":
        jobs = load_jobs()
        job = jobs.get("jobs", {}).get(getattr(args, "job", None) or "", {})
        is_agent = job.get("kind") == "agent"
        needs_sdk = (
            not is_agent
            and bool(getattr(args, "prompt", None) or job.get("prompt"))
        )
        if is_agent:
            _load_dotenv_file()
        cfg = load_config(require_api_key=needs_sdk)
        sys.exit(cmd_pipeline(cfg, args.job, args.prompt, args.tests))

    cfg = load_config(require_api_key=True)

    if args.command == "code":
        sys.exit(cmd_code(cfg, args.prompt))


if __name__ == "__main__":
    main()
