#!/usr/bin/env python3
"""Demo static server + editor save API (localhost only)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

RESULT_PORT = int(os.environ.get('DEMO_RESULT_PORT', '8769'))
DEMO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = Path(__file__).resolve().parent
PENDING = DEMO_ROOT / '.editor-pending-save.json'
RESULT = DEMO_ROOT / '.editor-save-result.json'
JS_DIR = (DEMO_ROOT / 'js').resolve()


class DemoHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DEMO_ROOT), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write('[demo-server] %s\n' % (fmt % args))

    def _path(self) -> str:
        return urlparse(self.path).path

    def _cors(self):
        origin = self.headers.get('Origin', '*')
        self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def end_headers(self):
        if self._path().startswith('/api/'):
            self._cors()
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def do_OPTIONS(self):
        if self._path().startswith('/api/'):
            self.send_response(204)
            self._cors()
            self.end_headers()
            return
        super().do_OPTIONS()

    def do_GET(self):
        path = self._path()
        if path == '/api/editor':
            self._json(200, {
                'ok': True,
                'save': True,
                'jsDir': 'js',
                'root': str(DEMO_ROOT),
            })
            return
        if path == '/api/save-result':
            self._json(404, {'ok': False, 'pending': True, 'error': '請改由結果埠讀取'})
            return
        super().do_GET()

    def do_POST(self):
        path = self._path()
        if path != '/api/save-js':
            self.send_error(404)
            return

        if self.client_address[0] not in ('127.0.0.1', '::1'):
            self._json(403, {'ok': False, 'error': '僅允許本機儲存'})
            return

        length = int(self.headers.get('Content-Length', 0))
        if length <= 0 or length > 8 * 1024 * 1024:
            self._json(400, {'ok': False, 'error': '請求內容無效'})
            return

        try:
            payload = json.loads(self.rfile.read(length).decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json(400, {'ok': False, 'error': 'JSON 格式錯誤'})
            return

        edits = payload.get('edits')
        if not isinstance(edits, list) or not edits:
            self._json(400, {'ok': False, 'error': '沒有可儲存的修改'})
            return

        for edit in edits:
            fname = edit.get('file')
            if fname not in {'scenes.js', 'choice-reactions.js', 'minigame-reactions.js', 'systems.js'}:
                self._json(400, {'ok': False, 'error': f'不允許寫入：{fname}'})
                return
            if not (JS_DIR / fname).is_file():
                self._json(400, {'ok': False, 'error': f'找不到檔案：js/{fname}'})
                return

        RESULT.unlink(missing_ok=True)
        try:
            PENDING.write_text(json.dumps({'edits': edits}, ensure_ascii=False), encoding='utf-8')
            env = os.environ.copy()
            env['DEMO_RESULT_PORT'] = str(RESULT_PORT)
            creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            subprocess.Popen(
                [sys.executable, str(TOOLS_DIR / 'editor_save.py')],
                cwd=str(DEMO_ROOT),
                env=env,
                creationflags=creationflags,
            )
        except OSError as exc:
            PENDING.unlink(missing_ok=True)
            self._json(500, {'ok': False, 'error': f'無法啟動儲存程序：{exc}'})
            return

        self._json(200, {
            'ok': True,
            'pending': True,
            'resultPort': RESULT_PORT,
            'message': '伺服器即將關閉，稍後寫入遊戲檔案',
        })
        threading.Thread(target=_shutdown_server, daemon=True).start()

    def _json(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)


_server_ref: ThreadingHTTPServer | None = None


def _shutdown_server():
    global _server_ref
    if _server_ref is not None:
        sys.stderr.write('[demo-server] shutting down for editor save\n')
        _server_ref.shutdown()
    os._exit(0)


def main():
    global _server_ref
    port = int(os.environ.get('DEMO_PORT', '8765'))
    try:
        _server_ref = ThreadingHTTPServer(('127.0.0.1', port), DemoHandler)
    except OSError as exc:
        print(f'demo-server: 無法啟動 port {port} — {exc}', file=sys.stderr, flush=True)
        print('請關閉佔用 8765 的舊 python 程序後重試。', file=sys.stderr, flush=True)
        sys.exit(1)

    print(f'demo-server: http://127.0.0.1:{port}/  (editor save API enabled)', flush=True)
    print(f'demo-server: js dir = {JS_DIR}', flush=True)
    try:
        _server_ref.serve_forever()
    except KeyboardInterrupt:
        print('\ndemo-server: stopped', flush=True)


if __name__ == '__main__':
    main()
