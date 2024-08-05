import sys
import requests
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette

# Function to check the status of a website
def check_website_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

# Main window class
class StatusChecker(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.url = "https://www.google.com"
        self.check_interval = 1  # Time interval between checks in milliseconds
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(self.check_interval)
        
        self.update_status()
    
    def initUI(self):
        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 24px;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        self.setWindowTitle('Online/Offline Status Checker')
        self.setGeometry(100, 100, 300, 100)
        self.show()
    
    def update_status(self):
        is_online = check_website_status(self.url)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if is_online:
            self.status_label.setText(f" online.")
            self.status_label.setStyleSheet("color: green; font-size: 24px;")
        else:
            self.status_label.setText(f" offline.")
            self.status_label.setStyleSheet("color: red; font-size: 24px;")

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    checker = StatusChecker()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
