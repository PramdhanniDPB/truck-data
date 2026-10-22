import subprocess
import time
from datetime import datetime

# =========================
# CONFIGURATION
# =========================

SCHEDULE = [
    "08:00",
    "09:19",
    "12:00",
    "17:00",
]

COMMAND = ".\\flow.bat"

# =========================
# SCHEDULER
# =========================

def run_command():
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Running: {COMMAND}")

    try:
        result = subprocess.run(
            COMMAND,
            shell=True,
            capture_output=True,
            text=True
        )

        print("Exit code:", result.returncode)

        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)

        if result.stderr:
            print("ERROR:")
            print(result.stderr)

    except Exception as e:
        print("Failed to execute command:", e)


def scheduler():
    executed_today = set()

    print("Scheduler started.")
    print("Schedule:", ", ".join(SCHEDULE))
    print("Command:", COMMAND)

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # Reset setiap hari
        if current_time == "00:00":
            executed_today.clear()

        if current_time in SCHEDULE and current_time not in executed_today:
            run_command()
            executed_today.add(current_time)

        time.sleep(1)


if __name__ == "__main__":
    scheduler()
