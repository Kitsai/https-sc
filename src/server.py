from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json


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
        if self.path == "/calculate":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            num1 = float(data.get("number1", 0))
            print(f"1: {num1}")
            num2 = float(data.get("number2", 0))
            print(f"2: {num2}")
            result = num1 + num2

            response_data = {"sum": result}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def log_message(self, format, *args):
        # Custom logging, override to control output
        print(
            f"{self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}"
        )


class HttpsServer(HTTPServer):
    address = ("localhost", 4443)

    def __init__(self) -> None:
        super().__init__(self.address, CustomHandler)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(certfile="./cert.pem", keyfile="./key.pem")
        self.socket = self.context.wrap_socket(self.socket, True)


if __name__ == "__main__":
    server = HttpsServer()
    print(f"Https Server rodando em https://{server.address[0]}:{server.address[1]}")
    server.serve_forever()
