import subprocess
import time

def run_youtube_qoe(video_url="https://www.youtube.com/watch?v=aqz-KE-bpKQ"):
    print("\n[ YouTube QoE Test Started ]")
    start_time = time.time()

    YTDLP_PATH = "/usr/local/bin/yt-dlp"

    try:
        video_direct_url = subprocess.check_output(
            [
                YTDLP_PATH,
                "--user-agent", "Mozilla/5.0",
                "-f", "best",
                "--no-playlist",
                "--get-url",
                video_url
            ],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=15
        ).strip()

        print(f"✅ Video URL Resolved:\n{video_direct_url[:80]}...")

        download_start = time.time()
        test = subprocess.run(
            ["curl", "-s", "--range", "0-1000000", video_direct_url],
            stdout=subprocess.DEVNULL,
            timeout=15
        )

        delay = (time.time() - download_start) * 1000
        total = (time.time() - start_time) * 1000

        print(f"📈 Startup Delay (first 1MB): {delay:.2f} ms")
        print(f"⏱️ Total Test Time        : {total:.2f} ms")

    except subprocess.CalledProcessError as e:
        print("❌ Failed to get video URL (yt-dlp error)")
        print("▶ Full yt-dlp output:\n", e.output)
    except Exception as e:
        print(f"❌ General Exception: {e}")

if __name__ == "__main__":
    run_youtube_qoe()