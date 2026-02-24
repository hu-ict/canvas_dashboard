import sys

from scripts.lib.lib_date import get_actual_date
from run_env_2 import run_env_2
from run_env_3 import run_env_3

if __name__ == "__main__":
    import os

    current_path = os.getcwd()
    print("Huidige pad:", current_path)

    sys.stdout.reconfigure(encoding="utf-8")
    l_actual_date = get_actual_date()
    run_env_2(l_actual_date)
    run_env_3(l_actual_date)

    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60

    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())
