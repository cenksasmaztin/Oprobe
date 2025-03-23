import time
import dns.resolver
import signal
import matplotlib.pyplot as plt
from threading import Event

# Kullanıcı tarafından programı durdurmak için bir event
stop_event = Event()

# Dünyada en çok kullanılan 5 sitenin adresleri
sites = ["google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com"]

# Test sonuçlarını saklamak için
results = {site: [] for site in sites}

# Signal handler
def signal_handler(sig, frame):
    print("\nTest sonlandırılıyor...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

def resolve_dns(dns_ip):
    """DNS IP adresi üzerinden sitelerin isim çözümleme süresini ölçer"""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_ip]

    while not stop_event.is_set():
        for site in sites:
            try:
                # DNS çözümleme zamanını ölç
                start_time = time.time()
                resolver.resolve(site, "A")  # A kaydı çözümleme
                resolve_time = (time.time() - start_time) * 1000  # ms cinsinden
            except Exception as e:
                resolve_time = None  # Hata durumunda çözümleme başarısız
                
            if resolve_time is not None:
                results[site].append(resolve_time)
                print(f"{site} çözümleme süresi: {resolve_time:.2f} ms")
            else:
                print(f"{site} çözümleme başarısız.")
        print("-" * 50)
        time.sleep(1)  # Bir sonraki ölçüm için kısa bir ara

def plot_results():
    """Test sonuçlarını grafikle raporlar"""
    plt.figure(figsize=(10, 6))
    for site, times in results.items():
        if times:
            plt.plot(times, label=site)
    plt.xlabel("Ölçüm Numarası")
    plt.ylabel("Çözümleme Süresi (ms)")
    plt.title("DNS Çözümleme Süreleri")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Kullanıcıdan DNS IP adresini al
    dns_ip = input("Lütfen test için DNS IP adresini girin: ")
    
    print("Test başlıyor... Programı durdurmak için Ctrl+C'ye basın.")
    
    try:
        resolve_dns(dns_ip)
    except KeyboardInterrupt:
        pass
    finally:
        # Program sonlandırıldığında sonuçları çiz
        print("Grafik oluşturuluyor...")
        plot_results()