import signal
import iperf3
import time
import matplotlib.pyplot as plt
from datetime import datetime

running = True
bandwidth_results = []
timestamps = []

def signal_handler(sig, frame):
    """Ctrl+C ile testi durdurma ve sonuçları kaydetme."""
    global running
    print("\nTest interrupted by user. Saving results...")
    save_bandwidth_results()
    plot_bandwidth_graph()
    running = False

def bandwidth_test(destination, reverse=False):
    """Bandwidth testi için iperf3 kullanır."""
    client = iperf3.Client()
    client.server_hostname = destination
    client.port = 5201
    client.protocol = 'tcp'
    client.duration = 1  # Her ölçüm için 1 saniyelik test süresi
    if reverse:
        client.reverse = True
    return client.run()

def save_bandwidth_results():
    """Bandwidth sonuçlarını log dosyasına kaydeder."""
    filename = f"bandwidth_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(filename, "w") as file:
        file.write("Timestamp,Upload (Mbps),Download (Mbps)\n")
        for ts, upload, download in bandwidth_results:
            file.write(f"{ts},{upload:.2f},{download:.2f}\n")
    print(f"Results saved to: {filename}")

def plot_bandwidth_graph():
    """Bandwidth sonuçlarını grafikleştirir."""
    if not bandwidth_results:
        print("No bandwidth data to plot.")
        return
    timestamps = [result[0] for result in bandwidth_results]
    upload = [result[1] for result in bandwidth_results]
    download = [result[2] for result in bandwidth_results]

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, upload, label="Upload (Mbps)", marker="o")
    plt.plot(timestamps, download, label="Download (Mbps)", marker="o")
    plt.xlabel("Time")
    plt.ylabel("Bandwidth (Mbps)")
    plt.title("Bandwidth Over Time")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f"bandwidth_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    print(f"Bandwidth graph saved to: {filename}")

def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)
    destination = input("Enter the destination IP or hostname: ")
    reverse_mode = input("Enable reverse mode? (y/n): ").lower() == "y"

    print("Starting bandwidth test. Press Ctrl+C to stop.")
    while running:
        try:
            result = bandwidth_test(destination, reverse=reverse_mode)
            if result and result.sent_Mbps and result.received_Mbps:
                timestamp = datetime.now().strftime("%H:%M:%S")
                bandwidth_results.append((timestamp, result.sent_Mbps, result.received_Mbps))
                print(f"[{timestamp}] Upload: {result.sent_Mbps:.2f} Mbps, Download: {result.received_Mbps:.2f} Mbps")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()