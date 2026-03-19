from http.server import BaseHTTPRequestHandler
import json
import requests
import base64

# ⚠️ NOTE: rembg এখানে অনেক সময় কাজ করবে না (memory issue)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs

        query = parse_qs(urlparse(self.path).query)
        image_url = query.get("url", [""])[0]

        if not image_url:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": False,
                "error": "No URL provided"
            }).encode())
            return

        try:
            # image download
            res = requests.get(image_url)
            img = res.content

            # ⚠️ dummy base64 (no bg remove এখানে)
            base64_img = base64.b64encode(img).decode()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": True,
                "remove_by": "Friend Vercel API",
                "image_base64": base64_img
            }).encode())

        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": False,
                "error": str(e)
            }).encode())
