"""
Scheduler: Runs the weather ETL pipeline every 10 minutes.
"""
import sys
import time
import subprocess
from datetime import datetime

import schedule


def job():
    """Execute the extract pipeline as a subprocess."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] Syncing weather data...")
    try:
        subprocess.run(
            [sys.executable, "pipeline/extract.py"],
            check=True,
            timeout=200,
        )
        print("Sync complete.")
    except subprocess.CalledProcessError as e:
        print(f"Pipeline error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


schedule.every(10).minutes.do(job)
print("Scheduler running (10 min interval). Press Ctrl+C to stop.")

job()  # Run once at startup

while True:
    schedule.run_pending()
    time.sleep(1)
