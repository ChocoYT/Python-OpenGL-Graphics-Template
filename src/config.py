import tomllib
from pathlib import Path
from typing import Any

root_path = Path(__file__).resolve().parent.parent

src_path    = root_path / "src"
config_path = src_path / "config.toml"

config: dict[str, Any] = {}

def load_config() -> None:
    global config
    
    with open(config_path, "rb") as f:
        config.update(tomllib.load(f))
