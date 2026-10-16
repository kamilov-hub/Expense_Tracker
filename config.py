from os import getenv, path
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = path.join(BASE_DIR, '.env')

load_dotenv(FILE_PATH)

class Setting:
    db_name: str = getenv("DB_NAME")
    db_user: str = getenv("DB_USER")
    db_password: str = getenv("DB_PASSWORD")
    db_host: str = getenv("DB_HOST")
    db_port: int = getenv("DB_PORT")

    def __repr__(self):
        return f"""
        Setting(db_name={self.db_name},
                db_user={self.db_user}, 
                db_password={self.db_password},
                db_host={self.db_host},
                db_port={self.db_port})"""


settings = Setting()