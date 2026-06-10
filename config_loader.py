import json
import os

_config_cache = None

def _load_config():
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    if not os.path.exists("config.json"):
        return {}

    try:
        with open("config.json","r") as f:
            _config_cache = json.load(f)

        return _config_cache
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return {}

def reload_config():
    """Force reload config after updates"""
    global _config_cache
    _config_cache = None
    return _load_config()

def get_api_key():
    return _load_config().get("groq_api_key","")

def get_username():
    return _load_config().get("username","")

def get_password():
    return _load_config().get("password","")