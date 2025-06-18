import os
from dataclasses import dataclass

@dataclass
class DBSettings:
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str

def get_settings(is_admin = False) -> DBSettings:
    return DBSettings(
        db_host=os.getenv("POSTGRES_HOST"),
        db_port=os.getenv("POSTGRES_PORT"),
        db_user=os.getenv(f"POSTGRES_{'ADMIN_' if is_admin else ''}USER"),
        db_password=os.getenv("POSTGRES_PASSWORD"),
        db_name=os.getenv("POSTGRES_DB"),
    )    
