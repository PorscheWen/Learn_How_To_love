#!/usr/bin/env python3
"""Nous Portal — Hermes Agent 本地門戶 HTTP 服務。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PORTAL_DIR = ROOT / "portal"
JOBS_PATH = ROOT / "jobs.json"
LOG_DIR = ROOT / ".portal-logs"
HERMES_PY = ROOT / "hermes.py"

_tasks: dict[str, dict] = {}
_tasks_lock = threading.Lock()


def _load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip())


def _portal_status() -> dict:
    api_key = os.environ.get("CURSOR_API_KEY", "").strip()
    nous_key = os.environ.get("NOUS_API_KEY", "").strip()
    game_cwd = Path(os.environ.get("HERMES_GAME_CWD", ROOT / "../../Ch1_Trust_Version3/Renpy_game")).resolve()
    api_doc = str((ROOT / "../../Ch1_Trust/Nous_Portal.md").resolve())
    cli_path = os.environ.get("HERMES_CLI_PATH", "").strip()
    if not cli_path:
        local = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "hermes-agent" / "venv" / "Scripts" / "hermes.exe"
        if local.is_file():
            cli_path = str(local)
    cli_exists = bool(cli_path and Path(cli_path).is_file())
    return {
        "name": "Nous Portal",
        "version": "1.2",
        "apiKeyDoc": api_doc,
        "hasApiKey": bool(api_key and not api_key.startswith("cursor_xxx")),
        "hasNousApiKey": bool(nous_key and not nous_key.startswith("sk-nous-xxx")),
        "hasHermesCli": cli_exists,
        "hermesCliPath": cli_path or None,
        "gameCwd": str(game_cwd),
        "gameCwdExists": game_cwd.is_dir(),
        "model": os.environ.get("HERMES_MODEL", "composer-2.5"),
        "agentModel": os.environ.get("HERMES_AGENT_MODEL", "google/gemini-2.5-pro"),
        "agentProvider": os.environ.get("HERMES_AGENT_PROVIDER", "nous"),
        "portalPort": int(os.environ.get("HERMES_PORTAL_PORT", "8780")),
    }


def _list_jobs() -> dict:
    with JOBS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _spawn_task(kind: str, args: list[str], label: str) -> str:
    task_id = uuid.uuid4().hex[:12]
    log_path = LOG_DIR / f"{task_id}.log"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with _tasks_lock:
        _tasks[task_id] = {
            "id": task_id,
            "kind": kind,
            "label": label,
            "status": "running",
            "exitCode": None,
            "startedAt": time.time(),
            "finishedAt": None,
            "logPath": str(log_path),
        }

    def runner() -> None:
        cmd = [sys.executable, str(HERMES_PY), *args]
        with log_path.open("w", encoding="utf-8") as log:
            log.write(f"$ {' '.join(cmd)}\n\n")
            log.flush()
            proc = subprocess.Popen(
                cmd,
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=os.environ.copy(),
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                log.write(line)
                log.flush()
            code = proc.wait()
        with _tasks_lock:
            t = _tasks[task_id]
            t["status"] = "finished" if code == 0 else "failed"
            t["exitCode"] = code
            t["finishedAt"] = time.time()

    threading.Thread(target=runner, daemon=True).start()
    return task_id


def _get_task(task_id: str) -> dict | None:
    with _tasks_lock:
        return _tasks.get(task_id)


def _read_log_tail(path: str, max_chars: int = 12000) -> str:
    p = Path(path)
    if not p.is_file():
        return ""
    text = p.read_text(encoding="utf-8", errors="replace")
    if len(text) <= max_chars:
        return text
    return "…(truncated)…\n" + text[-max_chars:]


class PortalHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print(f"[nous-portal] {self.address_string()} - {fmt % args}")

    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            index = PORTAL_DIR / "index.html"
            if not index.is_file():
                self.send_error(404, "portal/index.html missing")
                return
            body = index.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/status":
            self._send_json(200, _portal_status())
            return

        if path == "/api/jobs":
            self._send_json(200, _list_jobs())
            return

        if path.startswith("/api/tasks/"):
            task_id = path.split("/")[-1]
            task = _get_task(task_id)
            if not task:
                self._send_json(404, {"error": "task not found"})
                return
            payload = dict(task)
            payload["log"] = _read_log_tail(task["logPath"])
            self._send_json(200, payload)
            return

        self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        data = self._read_json()

        if path == "/api/test":
            scripts = data.get("scripts")
            args = ["test"]
            if scripts:
                args.extend(["--scripts", *scripts])
            task_id = _spawn_task("test", args, label="test")
            self._send_json(202, {"taskId": task_id})
            return

        if path == "/api/pipeline":
            job = data.get("job")
            if not job:
                self._send_json(400, {"error": "job required"})
                return
            jobs = _list_jobs().get("jobs", {})
            job_def = jobs.get(job, {})
            if job_def.get("kind") == "agent":
                args = ["agent", "--job", job]
                if data.get("prompt"):
                    args.extend(["--prompt", data["prompt"]])
                task_id = _spawn_task("agent", args, label=f"agent:{job}")
            else:
                task_id = _spawn_task("pipeline", ["pipeline", "--job", job], label=f"pipeline:{job}")
            self._send_json(202, {"taskId": task_id})
            return

        if path == "/api/agent":
            job = data.get("job")
            prompt = (data.get("prompt") or "").strip()
            if job:
                args = ["agent", "--job", job]
                if prompt:
                    args.extend(["--prompt", prompt])
                task_id = _spawn_task("agent", args, label=f"agent:{job}")
            elif prompt:
                toolsets = data.get("toolsets") or ["image_gen", "file", "terminal"]
                skills = data.get("skills") or []
                # 臨時 agent：寫入一次性 job 參數需擴充；目前僅支援 jobs.json
                self._send_json(400, {"error": "請指定 job（見 jobs.json 中 kind: agent）"})
                return
            else:
                self._send_json(400, {"error": "job required"})
                return
            self._send_json(202, {"taskId": task_id})
            return

        if path == "/api/code":
            prompt = (data.get("prompt") or "").strip()
            if not prompt:
                self._send_json(400, {"error": "prompt required"})
                return
            task_id = _spawn_task("code", ["code", prompt], label="code")
            self._send_json(202, {"taskId": task_id})
            return

        self.send_error(404)


def main() -> None:
    _load_dotenv()
    port = int(os.environ.get("HERMES_PORTAL_PORT", "8780"))
    host = os.environ.get("HERMES_PORTAL_HOST", "127.0.0.1")

    if not PORTAL_DIR.is_dir():
        sys.exit(f"缺少 portal 目錄: {PORTAL_DIR}")

    server = ThreadingHTTPServer((host, port), PortalHandler)
    url = f"http://{host}:{port}/"
    print(f"[nous-portal] Nous Portal 已啟動: {url}")
    print("[nous-portal] Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[nous-portal] 已停止")
        server.shutdown()


if __name__ == "__main__":
    main()
