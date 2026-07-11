import os
from pathlib import Path
from urllib.parse import quote_plus

import certifi
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Variabel {name} belum diisi di file .env")

    return value


class Config:
    SECRET_KEY = required_env("SECRET_KEY")

    # Konfigurasi Resend.
    RESEND_API_KEY = required_env("RESEND_API_KEY")

    RESEND_FROM_EMAIL = required_env("RESEND_FROM_EMAIL")

    CONTACT_RECEIVER_EMAIL = required_env("CONTACT_RECEIVER_EMAIL")

    TIDB_HOST = required_env("TIDB_HOST")
    TIDB_PORT = int(os.getenv("TIDB_PORT", "4000"))
    TIDB_USER = required_env("TIDB_USER")
    TIDB_PASSWORD = required_env("TIDB_PASSWORD")
    TIDB_DATABASE = required_env("TIDB_DATABASE")

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        f"{quote_plus(TIDB_USER)}:"
        f"{quote_plus(TIDB_PASSWORD)}@"
        f"{TIDB_HOST}:{TIDB_PORT}/"
        f"{TIDB_DATABASE}?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {
            "ssl": {
                "ca": certifi.where(),
                "check_hostname": True,
            }
        },
    }
