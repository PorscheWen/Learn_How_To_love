#!/usr/bin/env python3
"""Write pending editor edits to Demo/js/ (runs after demo-server exits)."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from editor_patch import apply_edits

DEMO_ROOT = Path(__file__).resolve().parent.parent
PENDING = DEMO_ROOT / '.editor-pending-save.json'
JS_DIR = DEMO_ROOT / 'js'
ALLOWED = frozenset({
    'scenes.js',
    'choice-reactions.js',
    'minigame-reactions.js',
    'systems.js',
})
RESULT = DEMO_ROOT / '.editor-save-result.json'


def _validate_js_sources(patched: dict[str, str], names: list[str]) -> None:
    import subprocess
    import tempfile

    for name in names:
        if name not in patched:
            continue
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.js', delete=False) as tmp:
            tmp.write(patched[name])
            tmp_path = tmp.name
        try:
            proc = subprocess.run(
                ['node', '--check', tmp_path],
                capture_output=True,
                text=True,
                timeout=15,
            )
            if proc.returncode != 0:
                detail = (proc.stderr or proc.stdout or '').strip().splitlines()
                hint = detail[0] if detail else '語法錯誤'
                raise ValueError(f'{name} 儲存後語法錯誤：{hint}')
        except FileNotFoundError:
            return
        finally:
            Path(tmp_path).unlink(missing_ok=True)


def main() -> int:
    time.sleep(0.35)
    if not PENDING.is_file():
        RESULT.write_text(json.dumps({
            'ok': False,
            'error': '找不到待儲存資料',
        }, ensure_ascii=False), encoding='utf-8')
        _serve_result_once()
        _restart_demo_server()
        return 1

    try:
        payload = json.loads(PENDING.read_text(encoding='utf-8'))
        edits = payload.get('edits') or []
        if not edits:
            raise ValueError('沒有可儲存的修改')

        sources: dict[str, str] = {}
        for edit in edits:
            fname = edit.get('file')
            if fname not in ALLOWED:
                raise ValueError(f'不允許寫入：{fname}')
            if fname not in sources:
                sources[fname] = (JS_DIR / fname).read_text(encoding='utf-8')

        patched, applied, failed = apply_edits(sources, edits)
        if not applied:
            raise ValueError('無法套用任何修改')

        saved: list[str] = []
        for fname in patched:
            if fname not in ALLOWED or fname not in sources:
                continue
            if patched[fname] == sources[fname]:
                continue
            (JS_DIR / fname).write_text(patched[fname], encoding='utf-8', newline='\n')
            saved.append(fname)

        if not saved:
            raise ValueError('修改內容與原檔相同，未寫入')

        _validate_js_sources(patched, saved)

        RESULT.write_text(json.dumps({
            'ok': True,
            'saved': saved,
            'applied': applied,
            'failed': failed,
        }, ensure_ascii=False), encoding='utf-8')
        _serve_result_once()
        _restart_demo_server()
        return 0
    except Exception as exc:  # noqa: BLE001
        RESULT.write_text(json.dumps({
            'ok': False,
            'error': str(exc),
        }, ensure_ascii=False), encoding='utf-8')
        _serve_result_once()
        _restart_demo_server()
        return 1
    finally:
        PENDING.unlink(missing_ok=True)


def _restart_demo_server() -> None:
    import subprocess

    demo = DEMO_ROOT / 'tools' / 'demo-server.py'
    env = os.environ.copy()
    env.setdefault('DEMO_PORT', '8765')
    env.setdefault('DEMO_RESULT_PORT', '8769')
    try:
        subprocess.Popen(
            [sys.executable, str(demo)],
            cwd=str(DEMO_ROOT),
            env=env,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
        )
    except OSError:
        pass


def _serve_result_once() -> None:
    import json as _json
    from http.server import BaseHTTPRequestHandler, HTTPServer

    result_port = int(os.environ.get('DEMO_RESULT_PORT', '8769'))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if urlparse(self.path).path != '/api/save-result':
                self.send_error(404)
                return
            try:
                body = RESULT.read_text(encoding='utf-8')
            except OSError:
                self.send_error(500)
                return
            payload = body.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, fmt, *args):
            return

    try:
        server = HTTPServer(('127.0.0.1', result_port), Handler)
        server.handle_request()
        server.server_close()
    except OSError:
        pass


if __name__ == '__main__':
    sys.exit(main())
