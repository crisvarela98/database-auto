import os
import shutil
import subprocess
from datetime import datetime
from config import BACKUP_DIR, LOG_DIR, DB_TYPE, SQLITE_DB_PATH, MONGO_DB_NAME

date = datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_folder = os.path.join(BACKUP_DIR, date)

os.makedirs(backup_folder, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "backup.log")

def log(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

try:

    if DB_TYPE == "sqlite":

        backup_path = os.path.join(backup_folder, "database.sqlite")
        shutil.copy(SQLITE_DB_PATH, backup_path)

        log("SQLite backup created")

    elif DB_TYPE == "mongo":

        command = [
            "mongodump",
            "--db",
            MONGO_DB_NAME,
            "--out",
            backup_folder
        ]

        subprocess.run(command)

        log("MongoDB backup created")

    zip_name = shutil.make_archive(backup_folder, "zip", backup_folder)

    log(f"Backup compressed: {zip_name}")

except Exception as e:

    log(f"Backup error: {e}")