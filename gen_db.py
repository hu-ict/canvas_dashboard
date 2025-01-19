import subprocess
import os

project_root = os.path.dirname(os.path.abspath(__file__))

scripts = [
    os.path.join(project_root, "src", "db","generate_data.py"),
]

def run_script(script_path):
    process = subprocess.run(["python", script_path], capture_output=True, text=True)

    print(f"Output from {os.path.basename(script_path)}:\n{process.stdout}")

    if process.stderr:
        print(f"Errors from {os.path.basename(script_path)}:\n{process.stderr}")

for script in scripts:
    print(f"\nRunning {os.path.basename(script)}")
    run_script(script)

print("All specified scripts have been executed sequentially.")
print("The application is now updated :)")