import os
import shutil
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_ROOT = os.path.join(BASE_DIR, "backups")

def make_backup():
    today = datetime.datetime.now().strftime("%Y%m%d")
    dest_dir = os.path.join(BACKUP_ROOT, today)
    os.makedirs(dest_dir, exist_ok=True)

    files_to_backup = [f for f in os.listdir(BASE_DIR) if f.endswith(".json") or f.endswith(".py")]

    for f in files_to_backup:
        src = os.path.join(BASE_DIR, f)
        dst = os.path.join(dest_dir, f)
        shutil.copy2(src, dst)

    print(f">>> 備份完成：{dest_dir}")

if __name__ == "__main__":
    make_backup()
