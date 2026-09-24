"""
Enterprise Expert Knowledge Worker Web Application & REST API Server.
Zero-external-dependency production server using the Python standard library http.server.
Serves the web UI and the real-time LangGraph REST endpoints.

Run:
    python3 app.py            # http://127.0.0.1:8000
    python3 app.py 8080       # custom port
    HOST=0.0.0.0 python3 app.py   # share on your network (see README security note)
"""

import sys
import os
import json
import traceback
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any

from dotenv import load_dotenv

load_dotenv()

# Ensure project root in python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.api import routes
from backend.api.routes import ApiError

FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Uploads travel as base64 inside JSON, so allow a little more than the 5 MB file limit
MAX_BODY_BYTES = 8 * 1024 * 1024


class KnowledgeWorkerRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    # ---------- helpers ----------
    def _send_json_response(self, data: Any, status: int = 200):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(response_bytes)

    def _send_error_json(self, status: int, message: str, extra: dict = None):
        payload = {"error": message}
        if extra:
            payload.update(extra)
        self._send_json_response(payload, status=status)

    def _dispatch(self, func, *args):
        """Run a route handler and translate exceptions into JSON errors."""
        try:
            self._send_json_response(func(*args))
        except ApiError as exc:
            self._send_error_json(exc.status, exc.message, exc.extra)
        except Exception:
            traceback.print_exc()
            self._send_error_json(500, "Internal server error. See the server console for details.")

    def _query(self):
        parsed = urllib.parse.urlparse(self.path)
        return parsed, {k: v[0] for k, v in urllib.parse.parse_qs(parsed.query).items()}

    # ---------- HTTP verbs ----------
    def do_GET(self):
        parsed, q = self._query()
        path = parsed.path.rstrip("/")
        parts = [p for p in path.split("/") if p]

        if path == "/api/sources":
            self._dispatch(routes.handle_get_sources)
        elif path == "/api/stats":
            self._dispatch(routes.handle_get_stats)
        elif path == "/api/faq":
            self._dispatch(routes.handle_get_faq)
        elif path == "/api/updates":
            self._dispatch(routes.handle_get_updates)
        elif path == "/api/document":
            self._dispatch(routes.handle_get_document, q.get("file", ""), q.get("role", "employee"))
        elif path == "/api/chats":
            self._dispatch(routes.handle_list_chats, q.get("role", "employee"))
        elif len(parts) == 3 and parts[:2] == ["api", "chats"]:
            self._dispatch(routes.handle_get_chat, parts[2], q.get("role", "employee"))
        elif path == "/api/activity":
            self._dispatch(routes.handle_get_activity)
        elif path == "/api/agents":
            self._dispatch(routes.handle_get_agents)
        elif path == "/api/evaluation":
            self._dispatch(routes.handle_get_evaluation)
        elif path == "/api/roles":
            self._dispatch(routes.handle_get_roles)
        elif path.startswith("/api/"):
            self._send_error_json(404, f"Endpoint '{path}' not found")
        else:
            # SPA routing: if the path is not a real file, serve index.html
            file_path = os.path.join(FRONTEND_DIR, parsed.path.lstrip("/"))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                super().do_GET()
            else:
                self.path = "/index.html"
                super().do_GET()

    def do_DELETE(self):
        parsed, q = self._query()
        parts = [p for p in parsed.path.rstrip("/").split("/") if p]
        if len(parts) == 3 and parts[:2] == ["api", "chats"]:
            self._dispatch(routes.handle_delete_chat, parts[2], q.get("role", "employee"))
        elif len(parts) == 3 and parts[:2] == ["api", "uploads"]:
            self._dispatch(routes.handle_delete_upload, parts[2], q.get("role", "employee"))
        else:
            self._send_error_json(404, f"Endpoint '{parsed.path}' not found")

    def do_POST(self):
        parsed, _ = self._query()
        path = parsed.path.rstrip("/")

        # Requiring JSON forces browsers to send a CORS pre-flight for cross-site requests,
        # which this server never approves. That blocks other websites from calling the API.
        if "application/json" not in self.headers.get("Content-Type", ""):
            self._send_error_json(415, "Content-Type must be application/json")
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self._send_error_json(400, "Invalid Content-Length header")
            return
        if content_length > MAX_BODY_BYTES:
            self._send_error_json(413, "Request body too large (limit 8 MB).")
            return

        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
            if not isinstance(body, dict):
                raise ValueError("JSON body must be an object")
        except Exception:
            self._send_error_json(400, "Invalid JSON in request body")
            return

        if path == "/api/chat":
            self._dispatch(routes.handle_chat_request, body)
        elif path == "/api/approval":
            self._dispatch(routes.handle_approval_request, body)
        elif path == "/api/upload":
            self._dispatch(routes.handle_upload, body)
        else:
            self._send_error_json(404, f"Endpoint '{path}' not found")

    def log_message(self, fmt, *args):
        # Keep the console readable: hide static file noise, show API calls
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)


def run_server(host: str = HOST, port: int = PORT):
    httpd = HTTPServer((host, port), KnowledgeWorkerRequestHandler)
    shown_host = "127.0.0.1" if host in ("0.0.0.0", "") else host
    url = f"http://{shown_host}:{port}"
    print("================================================================")
    print("  Enterprise Expert Knowledge Worker Web Server")
    print(f"  Open in your browser:  {url}")
    print(f"  Serving UI from:       {FRONTEND_DIR}")
    print("  Press Ctrl+C to stop")
    print("================================================================")
    
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Enterprise Knowledge Worker server.")
        httpd.server_close()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port=port_arg)
