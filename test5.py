import sys
import requests
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import psutil
from speedtest import Speedtest
import socket
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
import time

def check_website_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

# Encryption settings
KEY = b'sixteen byte key'  # Must be 16 bytes (128 bits)

def encrypt_data(data):
    """Encrypt the data using AES encryption"""
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data(encrypted_data):
    """Decrypt the data using AES decryption"""
    encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted.decode('utf-8')

# Store users' data in memory
user_data = []

class NetworkMonitor(QtWidgets.QWidget):  
    def __init__(self, username=None):
        super().__init__()
        self.username = username
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

        self.url = "https://www.google.com"
        self.check_interval = 1000  # Time interval between checks in milliseconds

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(self.check_interval)
        
        self.update_status()

    def initUI(self):
        self.setWindowTitle("Network Monitor")
        self.setGeometry(100, 100, 1200, 800)  # Increased height to accommodate the plot

        self.layout = QtWidgets.QVBoxLayout()

        self.welcome_label = QtWidgets.QLabel(f"Welcome, {self.username}!", self)
        self.layout.addWidget(self.welcome_label)

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

        self.inputArea = QtWidgets.QLineEdit(self)
        self.inputArea.setPlaceholderText("Enter IP to get details")
        self.layout.addWidget(self.inputArea)

        self.getIPButton = QtWidgets.QPushButton("Get IP Info", self)
        self.getIPButton.clicked.connect(self.getIP)
        self.layout.addWidget(self.getIPButton)

        self.resultarea = QtWidgets.QTextEdit(self)
        self.resultarea.setReadOnly(True)
        self.layout.addWidget(self.resultarea)

        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.status_label)

        # Create a FigureCanvasQTAgg object to embed the plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.time_stamps = []
        self.received_data = []
        self.sent_data = []
        self.max_length = 60

        self.ani = FuncAnimation(self.fig, self.update_plot, interval=1000)  # Update every second

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #000099;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
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

    def update_plot(self, frame):
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

        # Update the plot data
        current_time = time.strftime('%H:%M:%S')
        self.time_stamps.append(current_time)
        self.received_data.append(mb_new_received)
        self.sent_data.append(mb_new_sent)

        # Keep the length of the lists manageable
        if len(self.time_stamps) > self.max_length:
            self.time_stamps.pop(0)
            self.received_data.pop(0)
            self.sent_data.pop(0)

        self.ax.clear()
        self.ax.plot(self.time_stamps, self.received_data, label='MB Received', color='blue')
        self.ax.plot(self.time_stamps, self.sent_data, label='MB Sent', color='red')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('MB')
        self.ax.set_title('Network Data Usage Over Time')
        self.ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        self.canvas.draw()

    def update_status(self):
        is_online = check_website_status(self.url)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if is_online:
            self.status_label.setText(f"Online")
            self.status_label.setStyleSheet("color: green; font-size: 24px;")
        else:
            self.status_label.setText(f"Offline")
            self.status_label.setStyleSheet("color: red; font-size: 24px;")

    def getIP(self):
        target = self.inputArea.text()
        try:
            ip = socket.gethostbyname(target)
            ipinfo = requests.get(f"http://ip-api.com/json/{ip}").json()
            self.resultarea.setText(str(ipinfo))
        except:
            QMessageBox.warning(self, "Error", "Unable to fetch IP information")

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QtWidgets.QVBoxLayout()

        self.username_label = QtWidgets.QLabel("Username:", self)
        self.layout.addWidget(self.username_label)

        self.username_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.username_input)

        self.password_label = QtWidgets.QLabel("Password:", self)
        self.layout.addWidget(self.password_label)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_button)

        self.register_button = QtWidgets.QPushButton("Register", self)
        self.register_button.clicked.connect(self.handle_register)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        encrypted_password = encrypt_data(password)

        for user in user_data:
            if user['username'] == username and user['password'] == encrypted_password:
                self.hide()
                self.network_monitor = NetworkMonitor(username)
                self.network_monitor.show()
                return

        QMessageBox.warning(self, "Error", "Invalid username or password")

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        encrypted_password = encrypt_data(password)

        for user in user_data:
            if user['username'] == username:
                QMessageBox.warning(self, "Error", "Username already exists")
                return

        user_data.append({'username': username, 'password': encrypted_password})
        QMessageBox.information(self, "Success", "Registration successful")

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
