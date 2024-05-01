import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)


class Config:
    BULK_DATA_PATH: str = Path(os.environ.get('BULK_DATA_PATH'))
    WHITE_LIST_URL: str = os.environ.get('WHITE_LIST_URL')
    WAIT_TIME: float = float(os.environ.get('WAIT_TIME'))
    VISIBLE: bool = True if os.environ.get('VISIBLE').lower() == "true" else False


class DevelopConfig(Config):
    BULK_DATA_PATH = base_dir / 'data'
    VISIBLE = True


current_environ = os.environ.get('ENVIRON')

if current_environ == 'Production':
    config_obj = Config()
elif current_environ == 'Developing':
    config_obj = DevelopConfig()
else:
    config_obj = None
    raise ValueError("Wrong value for 'ENVIRON' parameter in .env file. Should be 'Production' or 'Developing'")


if __name__ == "__main__":
    print("This is not executive file my baby reindeer.\n\nPlease read README :)")
