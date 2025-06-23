# ntp_test.py

import ntplib
from time import time, ctime
from datetime import datetime

def run_ntp_test(server='pool.ntp.org'):
    ntp_client = ntplib.NTPClient()
    print(f"\n[ NTP Test Started ]")
    print(f"Target NTP Server: {server}")
    try:
        response = ntp_client.request(server, version=3)
        local_time = ctime(time())
        ntp_time = ctime(response.tx_time)
        delay_ms = response.delay * 1000
        offset_ms = response.offset * 1000

        print(f"Local Time      : {local_time}")
        print(f"NTP Time        : {ntp_time}")
        print(f"Round Trip Delay: {delay_ms:.3f} ms")
        print(f"Clock Offset    : {offset_ms:.3f} ms")

        # Optional thresholds
        if abs(offset_ms) > 500:
            print("⚠️  WARNING: Clock offset is critically high!")
        elif abs(offset_ms) > 100:
            print("ℹ️  NOTICE: Clock offset exceeds normal range.")

    except Exception as e:
        print(f"❌ NTP Test Failed: {e}")

if __name__ == "__main__":
    run_ntp_test()
    