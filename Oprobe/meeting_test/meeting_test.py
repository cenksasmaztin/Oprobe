import os
import time
import subprocess
import platform
import re
import matplotlib.pyplot as plt
from datetime import datetime

# Hedef sunucu adresleri
TARGET_SERVERS = {
    "Zoom": "zoom.us",
    "Teams": "teams.microsoft.com",
    "Google Meet": "meet.google.com"
}

# Raporların kaydedileceği klasör
REPORT_DIR = "meeting_test"

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ping_server(host):
    try:
        # İşletim sistemine göre ping komutu ayarlanır
        param = "-n" if platform.system().lower() == "windows" else "-c"
        cmd = ["ping", param, "1", host]
        output = subprocess.run(cmd, capture_output=True, text=True)
        latency = parse_latency(output.stdout)
        return latency
    except Exception as e:
        return None

def parse_latency(ping_output):
    # Latency değerlerini regex ile bulma
    latency_pattern = re.compile(r"time[=<]\s?(\d+\.?\d*)\s?ms")
    latencies = [float(match) for match in latency_pattern.findall(ping_output)]
    if latencies:
        return sum(latencies) / len(latencies)
    else:
        return None

def save_text_report(results):
    filename = os.path.join(REPORT_DIR, f"latency_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(filename, "w") as f:
        f.write("Latency Test Report\n")
        f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for server, data in results.items():
            f.write(f"Server: {server}\n")
            f.write(f"Average Latency: {sum(data['latencies']) / len(data['latencies']):.2f} ms\n")
            f.write(f"Details:\n")
            for ts, latency in zip(data['timestamps'], data['latencies']):
                f.write(f"  {ts} - {latency:.2f} ms\n")
            f.write("\n")
    print(f"Text report saved as {filename}")

def save_graph(results):
    plt.figure(figsize=(10, 6))
    for server, data in results.items():
        timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in data['timestamps']]
        plt.plot(timestamps, data['latencies'], label=server)
    plt.xlabel("Time")
    plt.ylabel("Latency (ms)")
    plt.title("Latency Test Results")
    plt.legend()
    plt.grid()
    graph_filename = os.path.join(REPORT_DIR, f"latency_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    plt.gcf().autofmt_xdate()  # Otomatik tarih formatı
    plt.savefig(graph_filename)
    print(f"Graph saved as {graph_filename}")

def main():
    # Ensure the report directory exists
    ensure_directory_exists(REPORT_DIR)

    results = {server: {"latencies": [], "timestamps": []} for server in TARGET_SERVERS}

    try:
        while True:
            print(f"Starting latency test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
            for server, host in TARGET_SERVERS.items():
                latency = ping_server(host)
                if latency is not None:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    results[server]["latencies"].append(latency)
                    results[server]["timestamps"].append(timestamp)
                    print(f"{server}: {latency:.2f} ms at {timestamp}")
            time.sleep(3)  # Her 3 saniyede bir test yapılır
    except KeyboardInterrupt:
        print("\nLatency test interrupted. Generating final report...")
        save_text_report(results)
        save_graph(results)
        print("Reports generated. Exiting.")

if __name__ == "__main__":
    main()