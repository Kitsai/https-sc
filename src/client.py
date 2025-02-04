import sys
import requests
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtWebChannel import QWebChannel


class HttpsClient:
    server = "https://localhost:4443"
    cert = "cert.pem"

    def constructor(self):
        self.app = QApplication(sys.argv)

        self.webview = QWebEngineView()

    def run(self):
        page = self.get_page()
        self.render(page)

    def get_page(self):
        try:
            response = requests.get(self.server, verify=self.cert)
            response.raise_for_status()
            html_content = response.text

            response = requests.get(self.server + "/style.css", verify=self.cert)
            response.raise_for_status()
            css_content = "<style>" + response.text + "</style>"

            if "</head>" in html_content:
                html_content = html_content.replace("</head>", css_content + "</head>")

            return html_content
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def render(self, html: str):
        self.webview.setHtml(html)
        self.webview.setWindowTitle("Sum Two Numbers")
        self.webview.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    client = HttpsClient()
    client.run()
