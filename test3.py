import time
import psutil
import speedtest
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize variables
last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

totalUsage = 0

# Initialize Speedtest
st = speedtest.Speedtest()
download_speed = st.download() / (1024 * 1024 * 8)
upload_speed = st.upload() / (1024 * 1024 * 8)
print('Download Speed: {:.2f} Mb'.format(download_speed))
print('Upload Speed: {:.2f} Mb'.format(upload_speed))
pin = st.results.ping
print(f'Ping: {pin}')

# Set up the plot
fig, ax = plt.subplots()
time_stamps = []
received_data = []
sent_data = []
max_length = 60  # Number of data points to display

def update_plot(frame):
    global last_received, last_sent, last_total, totalUsage

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
    print(f"{mb_new_received:.2f} MB received, {mb_new_sent:.2f} MB sent, {mb_new_total:.2f} MB total")
    print(f"Total Data Usage: {totalUsage:.2f} MB")

    # Update the plot data
    current_time = time.strftime('%H:%M:%S')
    time_stamps.append(current_time)
    received_data.append(mb_new_received)
    sent_data.append(mb_new_sent)

    # Keep the length of the lists manageable
    if len(time_stamps) > max_length:
        time_stamps.pop(0)
        received_data.pop(0)
        sent_data.pop(0)

    ax.clear()
    ax.plot(time_stamps, received_data, label='MB Received', color='blue')
    ax.plot(time_stamps, sent_data, label='MB Sent', color='red')
    ax.set_xlabel('Time')
    ax.set_ylabel('MB')
    ax.set_title('Network Data Usage Over Time')
    ax.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

# Create animation
ani = FuncAnimation(fig, update_plot, interval=1000)  # Update every second

plt.show()
