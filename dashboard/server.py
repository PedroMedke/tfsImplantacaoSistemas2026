from http.server import SimpleHTTPRequestHandler, HTTPServer

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'Dashboard OK')
            return
        return super().do_GET()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 80), DashboardHandler)
    print('Dashboard server running on http://0.0.0.0:80')
    server.serve_forever()
