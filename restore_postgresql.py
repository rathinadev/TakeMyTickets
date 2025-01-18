#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime
import subprocess
import logging
from pathlib import Path
import sys

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

# Logging setup
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "restore.log"

# Configure logging with both file and console output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # This will print to console as well
    ]
)

def perform_restore(backup_file):
    """
    Performs PostgreSQL database restore using environment variables
    and logs the process both to file and console.
    """
    backup_path = Path(backup_file)
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_file}")

    try:
        logging.info(f"Starting restore for database: {POSTGRES_DATABASE}")
        
        # Set up environment with password
        env = os.environ.copy()
        env["PGPASSWORD"] = POSTGRES_PASSWORD

        # Create a fresh database
        create_db_command = [
            "createdb",
            f"--host={POSTGRES_HOST}",
            f"--port={POSTGRES_PORT}",
            f"--username={POSTGRES_USER}",
            POSTGRES_DATABASE
        ]

        try:
            subprocess.run(create_db_command, env=env, check=True)
            logging.info(f"Created fresh database: {POSTGRES_DATABASE}")
        except subprocess.CalledProcessError:
            logging.warning(f"Database {POSTGRES_DATABASE} already exists. Proceeding with restore...")

        # Restore the backup
        if str(backup_file).endswith('.gz'):
            logging.info("Detected compressed backup file. Decompressing and restoring...")
            with subprocess.Popen(['gunzip', '--stdout', backup_file], stdout=subprocess.PIPE) as gunzip:
                restore_command = [
                    "psql",
                    f"--host={POSTGRES_HOST}",
                    f"--port={POSTGRES_PORT}",
                    f"--username={POSTGRES_USER}",
                    f"--dbname={POSTGRES_DATABASE}"
                ]
                restore_process = subprocess.run(restore_command, stdin=gunzip.stdout, env=env)
                if restore_process.returncode != 0:
                    raise subprocess.CalledProcessError(restore_process.returncode, restore_command)
        else:
            logging.info("Detected uncompressed backup file. Restoring...")
            restore_command = [
                "psql",
                f"--host={POSTGRES_HOST}",
                f"--port={POSTGRES_PORT}",
                f"--username={POSTGRES_USER}",
                f"--dbname={POSTGRES_DATABASE}",
                "-f", backup_file
            ]
            subprocess.run(restore_command, env=env, check=True)

        logging.info("Restore completed successfully!")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error during restore: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python restore_postgresql.py <backup_file_path>")
        sys.exit(1)

    backup_to_restore = sys.argv[1]

    try:
        perform_restore(backup_to_restore)
    except Exception as e:
        logging.error(f"Restore process failed: {e}")
        sys.exit(1)
