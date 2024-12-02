import os

from dotenv import load_dotenv
from envyaml import EnvYAML

_current_dir = os.path.dirname(__file__)

load_dotenv(os.path.join(_current_dir, "../../.env.local"))

CONFIG = EnvYAML(os.path.join(_current_dir, "config.yaml"))
