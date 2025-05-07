import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Default configuration settings
DEFAULT_CONFIG = {
    "ALICE_MODEL": "default",
    "ALICE_DEVICE_TYPE": "macos",  # Specify the device type to run on
    "ALICE_LANGUAGE": "zh-TW",  # Specify the response language of the agent
    "ALICE_API_KEY": None, # "your-api-key-here"
    "ALICE_TIMEOUT": 30,
    "ALICE_RETRIES": 3,
    "ALICE_BASE_URL": "https://openrouter.ai/api/v1",
    "ALICE_LOG_LEVEL": "INFO",
    "ALICE_SILENT_MODE": False
}

_config_cache: Dict[str, Any] = None  # Cache for configuration


def load_config() -> Dict[str, Any]:
    """Load configuration with priority:
    1. Local .env
    2. Home directory .env
    3. Environment variables
    4. Default values"""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    config = DEFAULT_CONFIG.copy()

    # 1. Load local .env (project root directory)
    local_env = Path(".env")
    if local_env.exists():
        load_dotenv(local_env)

    # 2. Load home directory .env (~/alice/.env)
    home_env = Path.home() / ".alice" / ".env"
    if home_env.exists():
        load_dotenv(home_env)

    # 3. Update configuration from environment variables
    for key in DEFAULT_CONFIG:
        env_value = os.getenv(key)
        if env_value is not None:
            # Special handling for boolean settings
            if key == "ALICE_SILENT_MODE":
                config[key] = env_value.lower() in ("true", "1", "yes", "on", "y")
            else:
                config[key] = env_value

    _config_cache = config
    return config


# Automatically load configuration when module is loaded
current_config = load_config()
