import time
import psutil
import speedtest

last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

totalUsage = 0

st = speedtest.Speedtest()

download_speed = st.download()
upload_speed = st.upload()
print('Download Speed: {:.2f} Mb'.format(download_speed / (1024 * 1024 * 8)))
print('Upload Speed: {:.2f} Mb'.format(upload_speed / (1024 * 1024 * 8)))

pin = st.results.ping
print(pin)

while True:
    bytes_received = psutil.net_io_counters().bytes_recv
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total = bytes_received + bytes_sent

    new_received = bytes_received - last_received
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total

    mb_new_received = new_received / 1024 / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024,

    print(f"{mb_new_received:.2f} MB recived, {mb_new_sent:.2f} MB sent, {mb_new_total:.2f} MB total")

    totalUsage += mb_new_total 
    print(f"{totalUsage:.2f} Total Data Usage")

    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

    time.sleep(1)

    print("1.1.1.1")        

    