# server.py
import os
import http.server
import socketserver
import json
from urllib.parse import unquote

PORT = int(os.environ.get("PORT", 8000))
WALLPAPER_DIR = "Wallpapers"
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/images":
            files = [f for f in os.listdir(WALLPAPER_DIR)
                     if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()
