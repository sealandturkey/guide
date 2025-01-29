import subprocess
import sys
import os

# Sanal ortam yolu
VENV_PATH = os.path.join(os.getcwd(), ".venv")

# Sanal ortamı aktif hale getir
if sys.platform == "win32":
    activate_script = os.path.join(VENV_PATH, "Scripts", "activate.bat")
else:
    activate_script = os.path.join(VENV_PATH, "bin", "activate")

# NGINX'i başlat
nginx_process = subprocess.Popen(
    ["C:/nginx/nginx.exe", "-c", os.getcwd()+"nginx.conf"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Django runserver başlat
try:
    subprocess.run(["python", "manage.py", "runserver"], check=True)
finally:
    # Django kapanınca NGINX'i durdur
    nginx_process.terminate()