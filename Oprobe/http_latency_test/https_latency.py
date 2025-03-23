import requests
import time
import os
from datetime import datetime

# Test edilecek HTTPS adresleri
HTTPS_LIST = [
    "https://www.google.com", "https://www.facebook.com", "https://www.amazon.com", 
    "https://www.yahoo.com", "https://www.wikipedia.org", "https://www.twitter.com", 
    "https://www.instagram.com", "https://www.linkedin.com", "https://www.microsoft.com", 
    "https://www.apple.com", "https://www.netflix.com", "https://www.reddit.com",
    "https://www.yandex.ru", "https://www.baidu.com", "https://www.bing.com", 
    "https://www.ebay.com", "https://www.bbc.co.uk", "https://www.cnn.com", 
    "https://www.espn.com", "https://www.spotify.com"
]

# Test sonuçlarını saklamak için listeler
test_results = []
timestamps = []

def perform_https_test():
    latencies = []
    for url in HTTPS_LIST:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)  # 10 saniyelik timeout ile GET isteği
            if response.status_code == 200:
                latency = (time.time() - start_time) * 1000  # ms cinsinden
                latencies.append(latency)
            else:
                latencies.append(None)  # Hatalı yanıt
        except requests.exceptions.RequestException:
            latencies.append(None)  # Hata durumunda None ekle
    return latencies

def save_results_to_file(test_number, latencies):
    avg_latency = sum([lat for lat in latencies if lat is not None]) / len([lat for lat in latencies if lat is not None])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder_path = "http_latency_test_result"
    os.makedirs(folder_path, exist_ok=True)
    report_path = os.path.join(folder_path, f"test_result_{test_number}.txt")

    with open(report_path, "w") as f:
        f.write(f"HTTPS Latency Test Report #{test_number}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        for url, latency in zip(HTTPS_LIST, latencies):
            f.write(f"{url}: {latency if latency is not None else 'Timeout'} ms\n")
        f.write(f"\nAverage Latency: {avg_latency:.2f} ms\n")

    return avg_latency

def main():
    test_number = 1
    while True:
        print(f"Starting Test #{test_number}")
        latencies = perform_https_test()
        avg_latency = save_results_to_file(test_number, latencies)

        # Terminale test sonuçlarını yazdır
        print(f"\nTest #{test_number} Results:")
        for url, latency in zip(HTTPS_LIST, latencies):
            print(f"{url}: {latency if latency is not None else 'Timeout'} ms")
        print(f"\nAverage Latency: {avg_latency:.2f} ms\n")

        test_results.append(avg_latency)
        timestamps.append(datetime.now().strftime("%H:%M:%S"))

        test_number += 1
        time.sleep(60)  # 1 dakika bekle

if __name__ == "__main__":
    main()
