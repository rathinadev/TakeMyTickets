#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime
import subprocess
import logging
from pathlib import Path

# Load environment variables from credentials.env
load_dotenv("credentials.env")

# Environment variables with validation
def get_env_or_raise(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"{var_name} is not defined in the credentials.env file.")
    return value

# Database configuration from environment
POSTGRES_HOST = get_env_or_raise("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = get_env_or_raise("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_or_raise("POSTGRES_PASSWORD")
POSTGRES_DATABASE = get_env_or_raise("POSTGRES_DATABASE")
BACKUP_PATH = get_env_or_raise("BACKUP_PATH")

# Logging setup
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "backup.log"

# Configure logging with both file and console output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # This will print to console as well
    ]
)

def perform_backup():
    """
    Performs PostgreSQL database backup using environment variables
    and logs the process both to file and console.
    """
    # Create backup directory if it doesn't exist
    backup_dir = Path(BACKUP_PATH)
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = backup_dir / f"{POSTGRES_DATABASE}_backup_{timestamp}.sql"

    try:
        logging.info(f"Starting backup for database: {POSTGRES_DATABASE}")
        
        # Construct the pg_dump command
        backup_command = [
            "pg_dump",
            f"--host={POSTGRES_HOST}",
            f"--port={POSTGRES_PORT}",
            f"--username={POSTGRES_USER}",
            f"--dbname={POSTGRES_DATABASE}",
            "--no-password",
            f"--file={backup_file}"
        ]

        # Set up environment with password
        env = os.environ.copy()
        env["PGPASSWORD"] = POSTGRES_PASSWORD

        # Execute backup
        subprocess.run(backup_command, check=True, env=env)
        
        # Log success
        logging.info(f"Backup completed successfully! File saved to: {backup_file}")

        # Optional: Compress the backup
        try:
            logging.info("Compressing backup file...")
            subprocess.run(['gzip', str(backup_file)], check=True)
            logging.info(f"Backup compressed successfully: {backup_file}.gz")
        except subprocess.CalledProcessError as e:
            logging.warning(f"Compression failed, but backup file is still intact: {e}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error during backup: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    try:
        perform_backup()
    except Exception as e:
        logging.error(f"Backup process failed: {e}")
        exit(1)
