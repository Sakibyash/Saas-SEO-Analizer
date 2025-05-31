from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    print(f"Server running at http://localhost:{port}")
    webbrowser.open(f"http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
