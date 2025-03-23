import subprocess
import os
import time
from datetime import datetime

# Flent'in RRUL testini çalıştıran bir fonksiyon
def run_rrul_test(server_ip, output_dir="flent_results", duration=300):
    """
    Flent ile RRUL testi yapar ve sonuçları bir klasöre kaydeder.
    
    :param server_ip: Netperf sunucusunun IP adresi.
    :param output_dir: Test sonuçlarının kaydedileceği dizin (varsayılan: flent_results).
    :param duration: Her bir testin süresi (varsayılan: 300 saniye).
    """
    # Çıktı klasörünü oluştur
    os.makedirs(output_dir, exist_ok=True)
    
    # Zaman damgası oluştur
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_file = os.path.join(output_dir, f"rrul_test_{timestamp}.txt")
    graph_file = os.path.join(output_dir, f"rrul_test_{timestamp}.png")
    
    # RRUL testi komutu
    command = [
        "flent", "rrul",
        "-H", server_ip,          # Netperf sunucusu IP adresi
        "-l", str(duration),      # Test süresi
        "-o", text_file           # Çıktı dosyasını metin olarak kaydet
    ]
    
    print(f"Running Flent RRUL test on {server_ip} for {duration} seconds...")
    print(f"Results will be saved to {text_file}")
    
    try:
        # Flent komutunu çalıştır ve text olarak kaydet
        subprocess.run(command, check=True)
        
        # Grafiği oluşturma komutu
        graph_command = [
            "flent", "-p", "box",  # Box plot grafiği oluştur
            "-o", graph_file,      # Çıktıyı PNG olarak kaydet
            text_file              # Kaydedilen test dosyasını kullan
        ]
        
        # Grafiği oluştur
        subprocess.run(graph_command, check=True)
        
        print(f"Test completed successfully.")
        print(f"Text results saved to {text_file}")
        print(f"Graph saved to {graph_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Flent RRUL test or generating graph: {e}")

# Ana program
if __name__ == "__main__":
    # Kullanıcıdan Netperf sunucusunun IP adresini iste
    server_ip = input("Enter the Netperf server IP address: ").strip()
    
    # Girilen IP adresini kontrol et
    if not server_ip:
        print("No IP address entered. Exiting.")
    else:
        print("Press Ctrl+C to stop the tests.")
        try:
            while True:
                # Her test için RRUL fonksiyonunu çağır
                run_rrul_test(server_ip)
                
                # 10 dakika bekle
                print("Waiting for 10 minutes before the next test...")
                time.sleep(10 * 60)  # 10 dakika (10 * 60 saniye)
        except KeyboardInterrupt:
            print("\nTesting stopped by user. Goodbye!")