# packet_loss_test.py

from ping3 import ping
import time

target = "8.8.8.8"
count = 30
timeout = 1
success = 0

print(f"Pinging {target} {count} times...\n")

for i in range(count):
    delay = ping(target, timeout=timeout)
    if delay is not None:
        print(f"Reply from {target}: time={round(delay * 1000, 2)} ms")
        success += 1
    else:
        print("Request timeout")
    time.sleep(1)

loss = ((count - success) / count) * 100
print(f"\nPacket loss: {loss:.2f}% ({count - success}/{count})")