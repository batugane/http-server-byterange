import os
from http.server import SimpleHTTPRequestHandler, HTTPServer


class RangeRequestHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            print(f"File not found: {path}")  # Log the missing file path
            return None
        try:
            fs = os.fstat(f.fileno())
            start, end = 0, fs.st_size
            if 'Range' in self.headers:
                self.send_response(206)
                ranges = self.headers['Range']
                print(f"Range request: {ranges}")  # Log the byte range request
                ranges = ranges.split('=')[1]
                ranges = ranges.split('-')
                if ranges[0]:
                    start = int(ranges[0])
                if ranges[1]:
                    end = int(ranges[1])
                else:
                    end = fs.st_size
                self.send_header('Content-Range', f'bytes {start}-{end - 1}/{fs.st_size}')
            else:
                self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(end - start))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
            self.end_headers()
            f.seek(start)
            return f
        except Exception as e:
            if f:
                f.close()
            print(f"Error during send_head: {e}")  # Log any exceptions
            raise

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Range")
        self.end_headers()

    def do_GET(self):
        print(f"GET request for {self.path}")  # Log the path requested
        try:
            super().do_GET()
        except ConnectionAbortedError:
            self.log_error("Connection aborted by client")
        except ConnectionResetError:
            self.log_error("Connection reset by client")
        except Exception as e:
            self.log_error(f"Unexpected error: {e}")

    def log_message(self, format, *args):
        print(f"{self.client_address} - - [{self.log_date_time_string()}] {format % args}")


def run(server_class=HTTPServer, handler_class=RangeRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
