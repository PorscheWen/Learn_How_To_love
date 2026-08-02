# -*- coding: utf-8 -*-
"""本機對話／旁白修改器伺服器（stdlib only）。"""
from __future__ import annotations

import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # Renpy_game/
SCRIPT = ROOT / "game" / "script.rpy"
PORT = 8787

sys.path.insert(0, str(HERE))
import dialogue_parser  # noqa: E402


def json_bytes(payload: dict, status: int = 200) -> tuple[int, bytes, str]:
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    return status, body, "application/json; charset=utf-8"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("[dialogue-editor] " + (fmt % args) + "\n")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            html = (HERE / "index.html").read_bytes()
            self._send(200, html, "text/html; charset=utf-8")
            return

        if path == "/api/meta":
            if not SCRIPT.exists():
                self._send(*json_bytes({"ok": False, "error": f"找不到 {SCRIPT}"}, 404))
                return
            sections = dialogue_parser.list_sections(SCRIPT)
            self._send(
                *json_bytes(
                    {
                        "ok": True,
                        "script": str(SCRIPT),
                        "mtime": SCRIPT.stat().st_mtime,
                        "sections": sections,
                    }
                )
            )
            return

        if path.startswith("/api/section/"):
            section_id = path[len("/api/section/") :].strip("/")
            try:
                data = dialogue_parser.load_section(SCRIPT, section_id)
                self._send(*json_bytes({"ok": True, "section": data}))
            except KeyError as exc:
                self._send(*json_bytes({"ok": False, "error": str(exc)}, 404))
            return

        self._send(*json_bytes({"ok": False, "error": "not found"}, 404))

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/save":
            try:
                payload = self._read_json()
                changes = payload.get("changes") or []
                result = dialogue_parser.apply_changes(SCRIPT, changes)
                result["mtime"] = SCRIPT.stat().st_mtime if SCRIPT.exists() else None
                status = 200 if result.get("ok") else 400
                self._send(*json_bytes(result, status))
            except Exception as exc:  # noqa: BLE001 — surface to UI
                self._send(*json_bytes({"ok": False, "error": str(exc)}, 500))
            return

        self._send(*json_bytes({"ok": False, "error": "not found"}, 404))


def main() -> None:
    if not SCRIPT.exists():
        print(f"[FAIL] 找不到 script：{SCRIPT}")
        raise SystemExit(1)

    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"對話修改器：{url}")
    print(f"腳本檔：{SCRIPT}")
    print("按 Ctrl+C 結束。")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已關閉。")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
