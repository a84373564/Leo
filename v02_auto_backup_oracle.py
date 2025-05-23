import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "modules")
BACKUP_ROOT = os.path.join(BASE_DIR, "backups")
KING_FILE = os.path.join(BASE_DIR, "king_pool.json")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def backup_all():
    today = datetime.now().strftime("%Y%m%d")
    backup_path = os.path.join(BACKUP_ROOT, today)
    ensure_dir(backup_path)

    if os.path.exists(MODULE_DIR):
        for fname in os.listdir(MODULE_DIR):
            if fname.endswith(".json"):
                full_path = os.path.join(MODULE_DIR, fname)
                shutil.copy2(full_path, os.path.join(backup_path, fname))

    if os.path.exists(KING_FILE):
        shutil.copy2(KING_FILE, os.path.join(backup_path, "king_pool.json"))

    print(f">>> 備份完成：{backup_path}")

if __name__ == "__main__":
    backup_all()
