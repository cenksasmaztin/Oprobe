import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

def run_traceroute(target):
    """Run traceroute command for a given target."""
    try:
        result = subprocess.run(['traceroute', target], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running traceroute:", e)
        return None

def parse_traceroute_output(output, timestamp):
    """Parse traceroute output to extract latency and hop information."""
    hop_pattern = re.compile(r"^\s*(\d+)\s+([\w\.-]+|\*)\s+\(?([\d\.]+)?\)?\s*(\d+\.\d+)?\s*ms?")
    hops = []

    for line in output.splitlines():
        match = hop_pattern.match(line)
        if match:
            hop_number = int(match.group(1))
            host = match.group(2) if match.group(2) != '*' else 'Timeout'
            ip = match.group(3) if match.group(3) else 'Unknown'
            latency = float(match.group(4)) if match.group(4) else None
            hops.append({
                'Timestamp': timestamp,
                'Hop': hop_number,
                'Host': host,
                'IP': ip,
                'Latency (ms)': latency
            })
    
    return hops

def print_hop_results(hops):
    """Print the traceroute hop results."""
    print("\nTraceroute Results:")
    for hop in hops:
        print(f"Hop {hop['Hop']}: {hop['Host']} ({hop['IP']}) - Latency: {hop['Latency (ms)']} ms")

def save_cumulative_results(cumulative_results, target):
    """Save all cumulative results to a timestamped CSV and PNG file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame(cumulative_results)

    # Save to CSV
    csv_filename = f"{target.replace('.', '_')}_cumulative_{timestamp}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Results saved to {csv_filename}")

    # Save to PNG
    plt.figure(figsize=(12, 7))
    for hop in df['Hop'].unique():
        hop_data = df[df['Hop'] == hop]
        plt.plot(hop_data['Timestamp'], hop_data['Latency (ms)'], marker='o', label=f"Hop {hop}: {hop_data['Host'].iloc[0]}")

    plt.title(f'Cumulative Latency Analysis for {target}')
    plt.xlabel('Timestamp')
    plt.ylabel('Latency (ms)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    png_filename = f"{target.replace('.', '_')}_cumulative_{timestamp}.png"
    plt.savefig(png_filename)
    plt.close()
    print(f"Graph saved to {png_filename}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python trace_latency.py <target-hostname-or-ip>")
        sys.exit(1)

    target = sys.argv[1]  # Target hostname or IP address
    cumulative_results = []  # Store results for all tests

    try:
        print(f"Starting traceroute to {target} every 6 seconds. Press CTRL+C to stop.")
        while True:
            print(f"\n--- Running traceroute for {target} ---")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output = run_traceroute(target)
            if output:
                hops = parse_traceroute_output(output, timestamp)
                print_hop_results(hops)  # Print results to terminal
                cumulative_results.extend(hops)  # Add current test to cumulative results
            else:
                print(f"Traceroute failed for {target}.")
            time.sleep(6)  # Wait for 6 seconds before running the next traceroute
    except KeyboardInterrupt:
        print("\nTraceroute monitoring stopped by user.")
        if cumulative_results:
            save_cumulative_results(cumulative_results, target)  # Save all results on exit
        else:
            print("No results to save.")