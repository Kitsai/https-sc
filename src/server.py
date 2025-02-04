from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests
        match self.path:
            case "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("src/page/index.html", "rb") as html_file:
                    self.wfile.write(html_file.read())
            case "/style.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("src/page/style.css", "rb") as css_file:
                    self.wfile.write(css_file.read())
            case _:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")

    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers["Content-Length"])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Read the POST data
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = f"<html><body><h1>POST request received!</h1><p>Data: {post_data.decode('utf-8')}</p></body></html>"
        self.wfile.write(response.encode("utf-8"))

    def log_message(self, format, *args):
        # Custom logging, override to control output
        print(
            f"{self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}"
        )


# Server setup
address = ("localhost", 4443)
server = HTTPServer(address, CustomHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="./cert.pem", keyfile="./key.pem")

server.socket = context.wrap_socket(server.socket, True)

print(f"Https Server rodando em https://{address[0]}:{address[1]}")
server.serve_forever()
