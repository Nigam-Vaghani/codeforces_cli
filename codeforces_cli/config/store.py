import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".cf_cli"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _secure_file_permissions(path: Path) -> None:
    if os.name != "nt":
        os.chmod(path, 0o600)


def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {}

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config(data: dict[str, Any]) -> None:
    _ensure_config_dir()
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    _secure_file_permissions(CONFIG_FILE)


def save_session(handle: str, cookies: dict[str, str]) -> None:
    config = load_config()
    config["handle"] = handle
    config["cookies"] = cookies
    save_config(config)


def get_session() -> tuple[str | None, dict[str, str]]:
    config = load_config()
    handle = config.get("handle")
    cookies = config.get("cookies", {})
    if not isinstance(cookies, dict):
        cookies = {}
    return handle, cookies


def clear_session() -> None:
    config = load_config()
    config.pop("handle", None)
    config.pop("cookies", None)
    save_config(config)
