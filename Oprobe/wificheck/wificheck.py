import subprocess
import re
import time
import socket
import os
from datetime import datetime
import statistics
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Color codes
RED = "\033[91m"
GREEN = "\033[92m"
ORANGE = "\033[93m"
RESET = "\033[0m"

# Data storage lists
timestamps = []
signal_strengths = []
snr_values = []
gtw_ping_times = []
int_ping_times = []
data_rates = []
throughputs = []
dhcp_results = []
dns_results = []
auth_results = []
wifi_performance_results = []

# Function to get the channel number based on frequency
def get_channel_from_frequency(freq):
    freq = int(freq)
    if 2400 <= freq <= 2500:
        return (freq - 2407) // 5
    elif 5000 <= freq <= 6000:
        return (freq - 5000) // 5
    return "N/A"

# Ping function and returning ping time
def ping(host):
    try:
        output = subprocess.check_output(["ping", "-I", "wlan0", "-c", "1", host], stderr=subprocess.STDOUT).decode('utf-8')
        match = re.search(r'time=(\d+\.\d+)', output)
        if match:
            return True, float(match.group(1))  # If ping is successful, return the time
        else:
            return False, None
    except subprocess.CalledProcessError:
        return False, None

# Gateway check (Ping the default gateway)
def gateway_check():
    try:
        output = subprocess.check_output(["ip", "route"]).decode('utf-8')
        gateway = re.search(r'default via ([\d.]+)', output)
        if gateway:
            return ping(gateway.group(1))  # Ping function returns true/false and time
        else:
            return False, None
    except subprocess.CalledProcessError:
        return False, None

# Internet ping check (Ping 8.8.8.8)
def internet_check():
    return ping("8.8.8.8")

# DHCP test function
def dhcp_check():
    try:
        output = subprocess.check_output(["ip", "addr", "show", "wlan0"]).decode('utf-8')
        if "inet " in output:
            return True  # DHCP successfully assigned IP
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# DNS test function
def dns_check():
    try:
        socket.gethostbyname('google.com')
        return True  # DNS resolved successfully
    except socket.gaierror:
        return False

# Authentication test function to get the current Wi-Fi authentication method using wpa_cli
def auth_check(interface='wlan0'):
    try:
        # Run the 'wpa_cli status' command to get Wi-Fi status details
        cmd = ["wpa_cli", "-i", interface, "status"]
        output = subprocess.check_output(cmd).decode('utf-8')

        # Check for encryption/authentication type using the 'key_mgmt' field
        if "WPA3" in output:
            return "WPA3"
        elif "WPA2" in output:
            return "WPA2"
        elif "WPA" in output:
            return "WPA"
        else:
            return "None"  # If no match is found, assume open network (None)
    except subprocess.CalledProcessError:
        return "Unknown"  # If the command fails or we can't retrieve the data

# Function to collect Wi-Fi device information
def get_wifi_info(interface='wlan0'):
    cmd = ["iw", "dev", interface, "station", "dump"]
    try:
        output = subprocess.check_output(cmd).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return []

    devices_info = []
    device_info = {}

    # Adding timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for line in output.split('\n'):
        if "Station" in line:
            if device_info:
                devices_info.append(device_info)
                device_info = {}
            device_info['MAC Address'] = line.split()[1]
        elif "signal:" in line:
            signal_strength = int(re.search(r"-?\d+", line).group(0))
            device_info['Signal Strength'] = signal_strength
        elif "tx bitrate:" in line:
            device_info['Data Rate'] = line.split(':')[1].strip()
        elif "rx bytes:" in line:
            throughput_bytes = int(line.split(':')[1].strip())  # Total bytes received
            throughput_mbps = (throughput_bytes * 8) / 1_000_000  # Convert from bytes to Mbps
            device_info['Throughput'] = throughput_mbps

    # Default noise level
    noise_level = -90  # dBm (This is a default value, real value can be added if found)

    # SNR calculation
    if 'Signal Strength' in device_info:
        signal_strength = device_info['Signal Strength']
        snr = signal_strength - noise_level
        device_info['SNR'] = snr
    else:
        device_info['SNR'] = "N/A"

    # Collect SSID, AP, frequency, and channel information
    ssid_cmd = ["iw", "dev", interface, "link"]
    try:
        ssid_output = subprocess.check_output(ssid_cmd).decode('utf-8')
        ssid_match = re.search(r'SSID: (.+)', ssid_output)
        ap_match = re.search(r'Connected to ([0-9a-fA-F:]+)', ssid_output)
        freq_match = re.search(r'freq: (\d+)', ssid_output)

        if ssid_match:
            device_info['SSID'] = ssid_match.group(1)
        else:
            device_info['SSID'] = "N/A"

        if ap_match:
            device_info['AP'] = ap_match.group(1)
        else:
            device_info['AP'] = "N/A"

        if freq_match:
            freq_value = freq_match.group(1)
            device_info['Frequency'] = f"{freq_value} MHz"
            device_info['Channel'] = get_channel_from_frequency(freq_value)
        else:
            device_info['Frequency'] = "N/A"
            device_info['Channel'] = "N/A"
    except subprocess.CalledProcessError:
        device_info['SSID'] = "N/A"
        device_info['AP'] = "N/A"
        device_info['Frequency'] = "N/A"
        device_info['Channel'] = "N/A"

    if device_info:
        device_info['Timestamp'] = timestamp  # Add timestamp
        devices_info.append(device_info)

    return devices_info

# Function to display real-time Wi-Fi info in a table format
def display_wifi_info():
    print("Real-Time Wi-Fi Analysis Started (Press CTRL+C to stop)")

    headers = [
        'Timestamp', 'MAC Address', 'SSID', 'AP', 'Frequency', 'Channel',
        'Signal Strength', 'Data Rate', 'Throughput',
        'SNR', 'GTW Ping', 'INT Ping', 'DHCP', 'DNS', 'Auth', 'WIFI Performance'
    ]

    # Print column headers
    header_format = "{:<20} {:<18} {:<8} {:<18} {:<12} {:<8} {:<15} {:<20} {:<25} {:<10} {:<10} {:<10} {:<7} {:<7} {:<7} {:<10}"
    print(header_format.format(*headers))

    try:
        while True:
            wifi_data = get_wifi_info()

            # Print data for each device
            for device in wifi_data:
                # Default performance status
                wifi_performance = "good"
                wifi_color = GREEN

                # Signal Strength check
                if device.get('Signal Strength', 'N/A') != "N/A":
                    signal_strength = device['Signal Strength']
                    if signal_strength >= -70:
                        wifi_performance = "poor"
                        wifi_color = ORANGE
                else:
                    # Connection loss
                    device['Signal Strength'] = 0
                    device['Data Rate'] = 0
                    device['Throughput'] = 0
                    device['SNR'] = 0
                    wifi_performance = "Failure (connection lost)"
                    wifi_color = RED

                # SNR check
                if device.get('SNR', 'N/A') != "N/A":
                    snr = device['SNR']
                    if snr >= 30:
                        wifi_performance = "poor"
                        wifi_color = ORANGE
                else:
                    wifi_performance = "Failure"
                    wifi_color = RED

                # Gateway ping check
                gateway_status, gateway_ping_time = gateway_check()
                if gateway_status:
                    gateway_ping_time_text = f"{gateway_ping_time:.2f} ms"
                    if gateway_ping_time > 12.00:
                        wifi_performance = "poor"
                        wifi_color = ORANGE
                else:
                    gateway_ping_time_text = "Failure"
                    wifi_performance = "Failure"
                    wifi_color = RED

                # Internet ping check
                internet_status, internet_ping_time = internet_check()
                if internet_status:
                    internet_ping_time_text = f"{internet_ping_time:.2f} ms"
                    if internet_ping_time > 50.00:
                        wifi_performance = "poor"
                        wifi_color = ORANGE
                else:
                    internet_ping_time_text = "Failure"
                    wifi_performance = "Failure"
                    wifi_color = RED

                # DHCP test
                if dhcp_check():
                    dhcp_status = "Success"
                else:
                    dhcp_status = "Failure"
                    wifi_color = RED

                # DNS test
                if dns_check():
                    dns_status = "Success"
                else:
                    dns_status = "Failure"
                    wifi_color = RED

                # Authentication test
                auth_status = auth_check()  # Get the used authentication method
                auth_results.append(auth_status)

                # Record the data
                timestamps.append(device.get('Timestamp', 'N/A'))
                signal_strengths.append(float(device.get('Signal Strength', 'N/A')))
                snr_values.append(float(device.get('SNR', 'N/A')))

                # 'Data Rate' check and append
                data_rate = device.get('Data Rate', 'N/A')
                if isinstance(data_rate, str):
                    data_rates.append(float(data_rate.replace(" MBit/s", "")))
                else:
                    data_rates.append(float(data_rate))  # If data is directly int

                # 'Throughput' check and append
                throughput = device.get('Throughput', 'N/A')
                if isinstance(throughput, str):
                    throughput_value = float(throughput.replace(" Mbps", ""))
                else:
                    throughput_value = throughput  # If data is directly int

                # Format the throughput to show only 2 decimal places and append "Mbps"
                formatted_throughput = f"{throughput_value:.2f} Mbps"
                throughputs.append(throughput_value)

                # Change 'Failure' to 0
                if gateway_ping_time_text != "Failure":
                    gtw_ping_times.append(float(gateway_ping_time_text.replace(" ms", "")))
                else:
                    gtw_ping_times.append(0)  # Replace 'Failure' with 0

                if internet_ping_time_text != "Failure":
                    int_ping_times.append(float(internet_ping_time_text.replace(" ms", "")))
                else:
                    int_ping_times.append(0)  # Replace 'Failure' with 0

                # DHCP, DNS, and Auth results
                dhcp_results.append(dhcp_status)
                dns_results.append(dns_status)
                auth_results.append(auth_status)

                wifi_performance_results.append(wifi_performance)

                row_format = "{:<20} {:<18} {:<8} {:<18} {:<12} {:<8} {:<15} {:<20} {:<25} {:<10} {:<10} {:<10} {:<7} {:<7} {:<7} {:<10}"
                print(row_format.format(
                    device.get('Timestamp', 'N/A'), device.get('MAC Address', 'N/A'), device.get('SSID', 'N/A'),
                    device.get('AP', 'N/A'), device.get('Frequency', 'N/A'), device.get('Channel', 'N/A'),
                    device.get('Signal Strength', 'N/A'), device.get('Data Rate', 'N/A'),
                    formatted_throughput, device.get('SNR', 'N/A'),
                    gateway_ping_time_text, internet_ping_time_text, dhcp_status, dns_status, auth_status, f"{wifi_color}{wifi_performance}{RESET}"
                ))

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nAnalysis stopped.")
        generate_summary_report()

# Function to generate the summary report
def generate_summary_report():
    if timestamps:
        duration = len(timestamps) * 5  # Total test duration (5 seconds per test)
        successful_tests = wifi_performance_results.count("good")
        poor_tests = wifi_performance_results.count("poor")
        failed_tests = wifi_performance_results.count("Failure")

        # Summary report
        print("\nTest Summary:")
        print(f"Total Test Duration: {duration} seconds")
        print(f"Average Signal Strength: {statistics.mean(signal_strengths):.2f} dB")
        print(f"Average SNR: {statistics.mean(snr_values):.2f} dB")
        print(f"Average Data Rate: {statistics.mean(data_rates):.2f} MBit/s")
        print(f"Average Throughput: {statistics.mean(throughputs):.2f} Mbps")
        print(f"Average Gateway Ping: {statistics.mean(gtw_ping_times):.2f} ms")
        print(f"Average Internet Ping: {statistics.mean(int_ping_times):.2f} ms")
        print(f"DHCP Status: {dhcp_results[-1]}")
        print(f"DNS Status: {dns_results[-1]}")
        print(f"Authentication Method: {auth_results[-1]}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Poor Tests: {poor_tests}")
        print(f"Failed Tests: {failed_tests}")

        # Created by message
        print("\nCreated by Oxoo Networks LLC.")

        # Create graph
        plt.figure(figsize=(10, 5))

        # Only show the start and end times on the time axis
        time_labels = [timestamps[0], timestamps[-1]]

        plt.plot(signal_strengths, label="Signal Strength (dB)", color="blue")
        plt.plot(snr_values, label="SNR (dB)", color="green")
        plt.plot(gtw_ping_times, label="Gateway Ping (ms)", color="orange")
        plt.plot(int_ping_times, label="Internet Ping (ms)", color="red")

        plt.title(f"Wi-Fi Performance Over Time\nCreated by Oxoo Networks LLC.")
        plt.xlabel("Test Time")
        plt.xticks([0, len(timestamps)-1], time_labels)  # Start and end times for x-axis
        plt.ylabel("Values")
        plt.legend()
        plt.grid(True)

        # Move the summary report to the bottom right corner of the graph
        summary_text = (
            f"Test Duration: {duration} s\n"
            f"Avg Signal Strength: {statistics.mean(signal_strengths):.2f} dB\n"
            f"Avg SNR: {statistics.mean(snr_values):.2f} dB\n"
            f"Avg Data Rate: {statistics.mean(data_rates):.2f} MBit/s\n"
            f"Avg Throughput: {statistics.mean(throughputs):.2f} Mbps\n"
            f"Avg Gateway Ping: {statistics.mean(gtw_ping_times):.2f} ms\n"
            f"Avg Internet Ping: {statistics.mean(int_ping_times):.2f} ms\n"
            f"DHCP: {dhcp_results[-1]}\n"
            f"DNS: {dns_results[-1]}\n"
            f"Auth: {auth_results[-1]}\n"
            f"Successful Tests: {successful_tests}\n"
            f"Poor Tests: {poor_tests}\n"
            f"Failed Tests: {failed_tests}"
        )
        plt.figtext(0.99, 0.05, summary_text, fontsize=10, verticalalignment='bottom', bbox=dict(facecolor='white', alpha=0.5), ha='right')

        # Check and create the folder if it doesn't exist
        if not os.path.exists('report'):
            os.makedirs('report')

        # Create file name with date and time
        file_name = datetime.now().strftime('report/report_%Y%m%d_%H%M%S.png')

        # Save the graph
        plt.savefig(file_name)

        # Show the graph
        plt.show()

        # Generate PDF
        generate_pdf_report(summary_text, file_name)

def generate_pdf_report(summary_text, graph_image):
    pdf_file_name = datetime.now().strftime('report/report_%Y%m%d_%H%M%S.pdf')
    c = canvas.Canvas(pdf_file_name, pagesize=letter)
    c.drawString(100, 750, "Wi-Fi Performance Report")
    c.drawString(100, 735, "Created by Oxoo Networks LLC")
    text = c.beginText(100, 700)
    text.textLines(summary_text)
    c.drawText(text)
    c.drawImage(graph_image, 100, 300, width=400, height=200)
    c.save()

# Start the program
display_wifi_info()