import subprocess
import sys
import os

def launch_gui():
    script_path = os.path.join(os.path.dirname(__file__), "main.py")
    subprocess.Popen([sys.executable, script_path])