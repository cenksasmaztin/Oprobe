
# Copyright (c) 2024  Cenk Sasmaztin <cenk@oxoonetworks.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.





# Jitter Test (Go)

This project is a simple **jitter measurement tool** written in Go. It performs a number of TCP connections to a specified host, measures the response time for each connection in **milliseconds**, and calculates the jitter — the average variation between consecutive delays.

##Purpose

**Jitter** refers to the variability in packet delay across a network. It is a critical metric for assessing network quality, especially for **real-time applications** like voice and video.

This tool:
- Opens TCP connections to a target host.
- Measures each response time in milliseconds.
- Calculates the jitter value.

## Requirements

- Go 1.16 or higher
- Internet access
- A reachable target host (default: `google.com:80`)

## Installation & Usage

1. Clone the repository or download `jitter.go`.

2. Navigate to the project directory in your terminal:
   ```bash
   cd ~/Documents/

3. Run the program:
go run jitter.go


4. Example output:
Starting jitter test (10 attempts):
Attempt  1: 43.78 ms
Attempt  2: 32.15 ms
...
Jitter: 3.406 ms


Configuration

You can customize the following parameters inside the code:
   •  target: The host and port to test (host:port format).
   •  attempts: Number of connection attempts.
   •  time.Sleep(...): Delay between each attempt.

Notes
   •  This tool uses TCP, not ICMP (ping). Jitter values may differ from traditional ping-based tools.
   •  It measures connection time only, not full data transmission.







TR

# Jitter Testi (Go)

Bu proje, Go programlama dili ile yazılmış basit bir **Jitter ölçüm uygulamasıdır**. Uygulama belirli sayıda TCP bağlantısı açarak her bir bağlantının yanıt süresini ölçer ve bu sürelerin değişkenliğini (jitter) milisaniye (ms) cinsinden hesaplar.

## Amaç

Jitter, iki ardışık gecikme arasındaki farktır. Ağ kalitesini belirlemede özellikle **gerçek zamanlı ses ve video uygulamaları** için önemli bir metriktir.

Bu araç:
- Belirtilen hedefe TCP bağlantıları gönderir.
- Yanıt sürelerini ms cinsinden ölçer.
- Jitter değerini hesaplar.

## Gereksinimler

- Go 1.16 veya üzeri
- İnternet bağlantısı
- Hedef IP veya hostname (varsayılan: `google.com:80`)

## Kurulum ve Kullanım

1. Depoyu klonlayın veya `jitter.go` dosyasını indirin.

2. Terminalde proje dizinine girin:
   ```bash
   cd ~/Documents/

3. Programı çalıştırın:
go run jitter.go


4. Örnek çıktı:
Jitter testi başlıyor (10 deneme):
Deneme  1: 43.78 ms
Deneme  2: 32.15 ms
...
Jitter: 3.406 ms

Yapılandırma

Kod içinde şu parametreleri değiştirebilirsiniz:
   •  target: Test yapılacak sunucu (host:port formatında).
   •  attempts: Kaç bağlantı yapılacağını belirler.
   •  time.Sleep(...): Her deneme arasındaki bekleme süresi.


Notlar
   •  TCP tabanlı olduğu için ICMP (ping) jitter’ı ile birebir aynı sonucu vermeyebilir.
   •  Uygulama, sadece bağlantı kurulabilirliği ve süresini ölçer; veri gönderimi yapmaz.
