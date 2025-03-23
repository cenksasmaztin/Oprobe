import signal
import subprocess
import time
import matplotlib.pyplot as plt
from datetime import datetime

running = True
latency_results = []
timestamps = []

def signal_handler(sig, frame):
    """Ctrl+C ile testi durdurma ve sonuçları kaydetme."""
    global running
    print("\nTest interrupted by user. Saving results...")
    save_latency_results()
    plot_latency_graph()
    running = False

def ping_test(destination):
    """Ping ile latency ölçümü yapar."""
    result = subprocess.run(
        ["ping", "-c", "1", destination],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode == 0:
        output = result.stdout
        latency = float(output.split("time=")[-1].split(" ms")[0])
        return latency
    else:
        print(f"Ping to {destination} failed.")
        return None

def save_latency_results():
    """Latency sonuçlarını log dosyasına kaydeder."""
    filename = f"latency_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(filename, "w") as file:
        file.write("Timestamp,Latency (ms)\n")
        for ts, latency in latency_results:
            file.write(f"{ts},{latency:.2f}\n")
    print(f"Results saved to: {filename}")

def plot_latency_graph():
    """Latency sonuçlarını grafikleştirir."""
    if not latency_results:
        print("No latency data to plot.")
        return
    timestamps = [result[0] for result in latency_results]
    latencies = [result[1] for result in latency_results]

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, latencies, label="Latency (ms)", marker="o")
    plt.xlabel("Time")
    plt.ylabel("Latency (ms)")
    plt.title("Latency Over Time")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f"latency_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    print(f"Latency graph saved to: {filename}")

def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)
    destination = input("Enter the destination IP or hostname: ")

    print("Starting latency test. Press Ctrl+C to stop.")
    while running:
        try:
            latency = ping_test(destination)
            if latency is not None:
                timestamp = datetime.now().strftime("%H:%M:%S")
                latency_results.append((timestamp, latency))
                print(f"[{timestamp}] Latency: {latency:.2f} ms")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()