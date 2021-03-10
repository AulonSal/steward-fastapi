from pydantic import BaseSettings as BS
from pathlib import Path

class BaseSettings(BS):
    # include some if needed
    pass

BASE_DIR = Path(__file__).resolve().parents[1]
INSTANCE_DIR = BASE_DIR.parent / 'instance'

