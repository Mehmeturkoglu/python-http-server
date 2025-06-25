from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

DOSYA_ADI = "mesajlar.txt"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/message":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)

                mesaj = data.get("mesaj", "").strip()
                if not mesaj:
                    raise ValueError("Mesaj bos")

                with open(DOSYA_ADI, "a", encoding='utf-8') as f:
                    f.write(mesaj + "\n")

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Mesaj kaydedildi.")
            except (json.JSONDecodeError, ValueError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Gecersiz JSON verisi veya bos mesaj.")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Sunucu hatasi: {str(e)}".encode())

    def do_GET(self):
        if self.path == "/message":
            try:
                mesajlar = []
                if os.path.exists(DOSYA_ADI):
                    with open(DOSYA_ADI, "r", encoding='utf-8') as f:
                        mesajlar = [line.strip() for line in f if line.strip()]

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(mesajlar).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Sunucu hatasi: {str(e)}".encode())

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Sunucu çalışıyor: http://localhost:8080")
    httpd.serve_forever()




