import time
import psutil
import speedtest
from speedtest import Speedtest
import requests
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread

class NetworkMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.last_received = psutil.net_io_counters().bytes_recv
        self.last_sent = psutil.net_io_counters().bytes_sent
        self.last_total = self.last_received + self.last_sent

        self.totalUsage = 0

        self.download_speed = 0
        self.upload_speed = 0
        self.ping = 0

        self.update_speedtest()
        self.update_network_usage()

    def initUI(self):
        self.setWindowTitle("Network Monitor")
        self.setGeometry(100, 100, 1200, 600)

        self.layout = QtWidgets.QVBoxLayout()

        self.download_label = QtWidgets.QLabel("Download Speed: Calculating...", self)
        self.layout.addWidget(self.download_label)

        self.upload_label = QtWidgets.QLabel("Upload Speed: Calculating...", self)
        self.layout.addWidget(self.upload_label)

        self.ping_label = QtWidgets.QLabel("Ping: Calculating...", self)
        self.layout.addWidget(self.ping_label)

        self.usage_label = QtWidgets.QLabel("Data Usage: 0.00 MB received, 0.00 MB sent, 0.00 MB total", self)
        self.layout.addWidget(self.usage_label)

        self.total_usage_label = QtWidgets.QLabel("Total Data Usage: 0.00 MB", self)
        self.layout.addWidget(self.total_usage_label)

        self.ip_label = QtWidgets.QLabel("My IP Address: Calculating...", self)
        self.layout.addWidget(self.ip_label)

        self.latency_area = QtWidgets.QTextEdit(self)
        self.latency_area.setReadOnly(True)
        self.layout.addWidget(self.latency_area)

        self.inputArea = QtWidgets.QLineEdit(self)
        self.inputArea.setPlaceholderText("Enter IP to get details")
        self.layout.addWidget(self.inputArea)

        self.getIPButton = QtWidgets.QPushButton("Get IP Info", self)
        self.getIPButton.clicked.connect(self.getIP)
        self.layout.addWidget(self.getIPButton)

        self.resultarea = QtWidgets.QTextEdit(self)
        self.resultarea.setReadOnly(True)
        self.layout.addWidget(self.resultarea)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #000099;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                font-size: 14px;
                padding: 5px;
                background-color:  #001a00;
                color: #00e600;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QWidget {
                background-color: #f7f7f7;
            }
        """)

    def update_speedtest(self):
        st = Speedtest()
        self.download_speed = st.download() / (1024 * 1024 * 8)
        self.upload_speed = st.upload() / (1024 * 1024 * 8)
        self.ping = st.results.ping

        self.download_label.setText(f"Download Speed: {self.download_speed:.2f} Mb")
        self.upload_label.setText(f"Upload Speed: {self.upload_speed:.2f} Mb")
        self.ping_label.setText(f"Ping: {self.ping:.2f} ms")

        # Change color based on values
        if self.download_speed < 10:
            self.download_label.setStyleSheet("color: red;")
        else:
            self.download_label.setStyleSheet("color: green;")

        if self.upload_speed < 5:
            self.upload_label.setStyleSheet("color: red;")
        else:
            self.upload_label.setStyleSheet("color: green;")

        if self.ping > 100:
            self.ping_label.setStyleSheet("color: red;")
        else:
            self.ping_label.setStyleSheet("color: green;")

        self.latency_area.setText(f"Download Speed: {self.download_speed:.2f} Mb\n"
                                  f"Upload Speed: {self.upload_speed:.2f} Mb\n"
                                  f"Ping: {self.ping:.2f} ms")

    def update_network_usage(self):
        bytes_received = psutil.net_io_counters().bytes_recv
        bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_total = bytes_received + bytes_sent

        new_received = bytes_received - self.last_received
        new_sent = bytes_sent - self.last_sent
        new_total = bytes_total - self.last_total

        mb_new_received = new_received / 1024 / 1024
        mb_new_sent = new_sent / 1024 / 1024
        mb_new_total = new_total / 1024 / 1024

        self.totalUsage += mb_new_total

        self.usage_label.setText(f"{mb_new_received:.2f} MB received, {mb_new_sent:.2f} MB sent, {mb_new_total:.2f} MB total")
        self.total_usage_label.setText(f"Total Data Usage: {self.totalUsage:.2f} MB")

        self.last_received = bytes_received
        self.last_sent = bytes_sent
        self.last_total = bytes_total

        hostname = socket.gethostname()
        myip = socket.gethostbyname(hostname)
        self.ip_label.setText(f"My IP Address: {myip}")

        QtCore.QTimer.singleShot(1000, self.update_network_usage)

    def getIP(self):
        ipp = str(self.inputArea.text())
        linkURl = "https://api.techniknews.net/ipgeo/"
        try:
            respond = requests.get(linkURl + ipp).json()
            ip = respond['ip']
            status = respond['status']
            continent = respond['continent']
            country = respond['country']
            countryCode = respond['countryCode']
            regionName = respond['regionName']
            city = respond['city']
            zip = respond['zip']
            lat = respond['lat']
            lon = respond['lon']
            timezone = respond['timezone']
            currency = respond['currency']
            isp = respond['isp']
            org = respond['org']
            mobile = respond['mobile']
            proxy = respond['proxy']

            finalResult = (
                f'IP : {ip}\nStatus : {status}\nContinent : {continent}\nCountry : {country}\nCountryCode : {countryCode}\n'
                f'RegionName : {regionName}\nCity : {city}\nZip : {zip}\nLat : {lat}\nLon : {lon}\nTimezone : {timezone}\n'
                f'Currency : {currency}\nISP : {isp}\nOrg : {org}\nMobile : {mobile}\nProxy : {proxy}\n\n'
            )

            self.resultarea.setText(finalResult)
        except:
            finalResult = "Not found. Try another IP"
            self.resultarea.setText(finalResult)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    monitor = NetworkMonitor()
    monitor.show()
    app.exec_()
