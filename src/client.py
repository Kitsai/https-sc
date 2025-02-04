import sys
import requests
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel


server = "https://localhost:4443"
cert = "cert.pem"


class Bridge(QObject):
    resultReady = pyqtSignal(float)
    receivedInput = pyqtSignal(object)

    @pyqtSlot(str, str)
    def sendData(self, num1, num2):
        try:
            number1 = float(num1)
            number2 = float(num2)
            self.receivedInput.emit((number1, number2))
        except ValueError:
            print("Invalid input")
            return

    def returnResult(self, val: float):
        self.resultReady.emit(val)


class HttpsClient:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.web_view = QWebEngineView()

        self.page = QWebEnginePage()
        self.web_view.setPage(self.page)

        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("bridge", self.bridge)
        self.page.setWebChannel(self.channel)

        self.bridge.receivedInput.connect(lambda result: self.calculate(result))

        self.bridge.resultReady.connect(
            lambda result: self.page.runJavaScript(f"displayResult({result});")
        )

    def run(self):
        page = self.get_page()
        self.render(page)

    def get_page(self):
        try:
            response = requests.get(server, verify=cert)
            response.raise_for_status()
            html_content = response.text

            response = requests.get(server + "/style.css", verify=cert)
            response.raise_for_status()
            css_content = "<style>" + response.text + "</style>"

            if "</head>" in html_content:
                html_content = html_content.replace("</head>", css_content + "</head>")

            return html_content
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def render(self, html: str):
        self.web_view.setHtml(html)
        self.web_view.setWindowTitle("Sum Two Numbers")
        self.web_view.show()
        sys.exit(self.app.exec_())

    def calculate(self, nums):
        print(nums)
        number1, number2 = nums
        server_url = f"{server}/calculate"
        payload = {"number1": number1, "number2": number2}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                server_url, json=payload, headers=headers, verify=cert
            )
            response.raise_for_status()
            data = response.json()
            result = data.get("sum", 0)

            self.bridge.returnResult(result)
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with server: {e}")


if __name__ == "__main__":
    client = HttpsClient()
    client.run()
