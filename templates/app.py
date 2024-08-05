from flask import Flask, jsonify, render_template
import time
import psutil
import speedtest

app = Flask(__name__)

last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

totalUsage = 0

st = speedtest.Speedtest()
download_speed = st.download() / (1024 * 1024 * 8)
upload_speed = st.upload() / (1024 * 1024 * 8)
ping = st.results.ping

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/network_data')
def network_data():
    global last_received, last_sent, last_total, totalUsage, download_speed, upload_speed, ping

    bytes_received = psutil.net_io_counters().bytes_recv
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total = bytes_received + bytes_sent

    new_received = bytes_received - last_received
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total

    mb_new_received = new_received / 1024 / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024

    totalUsage += mb_new_total

    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

    data = {
        'download_speed': download_speed,
        'upload_speed': upload_speed,
        'ping': ping,
        'mb_new_received': mb_new_received,
        'mb_new_sent': mb_new_sent,
        'mb_new_total': mb_new_total,
        'totalUsage': totalUsage
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
