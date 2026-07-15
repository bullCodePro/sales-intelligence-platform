from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from packages.companies.repository import create_company, list_companies
from packages.contacts.repository import create_contact, list_contacts
from packages.exports.csv_export import to_csv
from packages.scoring.service import list_scores
from packages.shared.config import settings
from packages.shared.db import ensure_database

WEB_ROOT = Path(__file__).resolve().parents[1] / "web"


class ApiHandler(BaseHTTPRequestHandler):
    server_version = "SalesIntelligenceHTTP/0.1"

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json({"status": "ok"})
        elif path == "/api/companies":
            self.send_json({"companies": list_companies()})
        elif path == "/api/contacts":
            self.send_json({"contacts": list_contacts()})
        elif path == "/api/scores":
            self.send_json({"scores": list_scores()})
        elif path == "/api/export/companies.csv":
            self.send_csv("companies.csv", to_csv(list_companies()))
        else:
            self.serve_static(path)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            payload = self.read_json()
            if path == "/api/companies":
                self.send_json({"company": create_company(payload)}, HTTPStatus.CREATED)
            elif path == "/api/contacts":
                self.send_json({"contact": create_contact(payload)}, HTTPStatus.CREATED)
            else:
                self.send_json({"error": "Route not found"}, HTTPStatus.NOT_FOUND)
        except ValueError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw_body = self.rfile.read(length).decode("utf-8")
        return json.loads(raw_body)

    def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_csv(self, filename: str, body_text: str) -> None:
        body = body_text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_static(self, path: str) -> None:
        relative_path = "index.html" if path == "/" else path.lstrip("/")
        file_path = (WEB_ROOT / relative_path).resolve()

        if WEB_ROOT not in file_path.parents and file_path != WEB_ROOT:
            self.send_error(HTTPStatus.FORBIDDEN)
            return

        if not file_path.exists() or file_path.is_dir():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        body = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    ensure_database()
    server = ThreadingHTTPServer((settings.host, settings.port), ApiHandler)
    print(f"Sales Intelligence Platform running at http://{settings.host}:{settings.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
