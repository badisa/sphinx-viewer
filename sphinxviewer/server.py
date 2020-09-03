import os
import webbrowser
from typing import Dict

from http.server import HTTPServer, BaseHTTPRequestHandler

from sphinxviewer.sphinx import build_html

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


class RequestHandler(BaseHTTPRequestHandler):

    STATIC_PATH = "_static"
    BUILD_PATH = "_build"

    def do_GET(self):
        if self.path == "/":
            self.serve_index()
        elif self.path.startswith("/rst/"):
            self.serve_rst()
        elif self.path.startswith("/html/"):
            self.serve_html()
        elif self.path.startswith(f"/{self.STATIC_PATH}/"):
            self.serve_static()
        else:
            self.error_resp()

    def do_POST(self):
        if self.path.startswith("/rst/"):
            self.update_rst()
        elif self.path.startswith("/html/"):
            self.build_html()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL")

    def parse_form_data(self) -> Dict[str, str]:
        # Hacky dumpster fire of hackery
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode("utf-8")
        content_type = self.headers["Content-Type"]
        boundary_index = content_type.find("boundary=")
        boundary = content_type[boundary_index + len("boundary="):]
        parts = body.split(boundary)
        if len(parts) != 3:
            print("WOOPS")
        data = parts[1]
        field_vals = {}
        fields = [part for part in data.split("name=") if part.startswith("\"")]
        for field in fields:
            field_parts = field.split("\r\n")
            parts = [part for part in field_parts if part]
            if not len(parts):
                continue
            if len(parts) % 2 != 0:
                parts = parts[:-1]
            field_vals[parts[0].strip("\"")] = parts[1]
        return field_vals

    def serve_index(self):
        self.send_response(200)
        self.end_headers()
        with open(os.path.join(TEMPLATES_DIR, "index.html"), "rb") as ifs:
            self.wfile.write(ifs.read())

    def serve_static(self):
        cur_dir = os.getcwd()
        path = self.path[1:]  # Strip off the leading slash
        static_path = os.path.join(cur_dir, self.BUILD_PATH, "html", path)
        if os.path.isfile(static_path):
            self.send_response(200)
            self.end_headers()
            with open(static_path, "rb") as ifs:
                self.wfile.write(ifs.read())
        else:
            self.error_resp()

    def build_html(self):
        path = self.path[len("/html/"):]
        paths_to_build = None
        if path:
            paths_to_build = [path + ".rst"]
        success = build_html(os.getcwd(), "_build", files=paths_to_build)
        if success:
            self.send_response(201)
            self.end_headers()
        else:
            self.error_resp()

    def update_rst(self):
        data = self.parse_form_data()
        text_data = data.get("text", None)
        cur_dir = os.getcwd()
        path = self.path[len("/rst/"):]
        rst_path = os.path.join(cur_dir, path)
        if not rst_path.endswith(".rst"):
            rst_path = rst_path + ".rst"
        if text_data and os.path.isfile(rst_path):
            self.send_response(201)
            self.end_headers()
            # Change this to write
            with open(rst_path, "w") as ofs:
                ofs.write(text_data)
        else:
            self.error_resp()

    def serve_html(self):
        cur_dir = os.getcwd()
        path = self.path[len("/html/"):]
        html_path = os.path.join(cur_dir, self.BUILD_PATH, "html", path)
        if not html_path.endswith(".html"):
            html_path = html_path + ".html"
        if os.path.isfile(html_path):
            self.send_response(200)
            self.end_headers()
            with open(html_path, "rb") as ifs:
                self.wfile.write(ifs.read())
        else:
            self.error_resp()

    def serve_rst(self):
        cur_dir = os.getcwd()
        path = self.path[len("/rst/"):]
        rst_path = os.path.join(cur_dir, path)
        if not rst_path.endswith(".rst"):
            rst_path = rst_path + ".rst"
        if os.path.isfile(rst_path):
            self.send_response(200)
            self.end_headers()
            with open(rst_path, "rb") as ifs:
                self.wfile.write(ifs.read())
        else:
            self.error_resp()

    def error_resp(self):
        self.send_response(500)
        self.end_headers()
        self.wfile.write(b"Welp")


def serve_server(port: int, browser: bool = True):
    httpd = HTTPServer(("localhost", port), RequestHandler)
    if browser:
        webbrowser.open(f"http://localhost:{port}/")
    httpd.serve_forever()
