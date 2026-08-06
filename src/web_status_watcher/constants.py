from pathlib import Path

PROJECT_ROOT = Path.cwd()

CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

CONFIG_FILE = CONFIG_DIR / "config.yaml"
DATABASE_FILE = DATA_DIR / "webstatuswatcher.db"

DEFAULT_CHECK_INTERVAL = 30

LOG_FILE = LOG_DIR / "application.log"
