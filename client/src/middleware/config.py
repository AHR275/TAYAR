import json
import os

# get absolute path to config.json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "secrets", "config.json")

# load config
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)