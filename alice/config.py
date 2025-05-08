import os
import sys
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import argparse

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

def parse_cli_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-s", "--silent", action="store_true", help="Enable silent mode")
    # Add more options here if needed
    args, _ = parser.parse_known_args(sys.argv[1:])
    return args

def load_config() -> Dict[str, Any]:
    """
    Load configuration with priority:
    1. Command line options
    2. Local .env
    3. Home directory .env
    4. Environment variables
    5. Default values
    """
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

    # 4. Override with command line arguments (highest priority)
    args = parse_cli_args()
    if getattr(args, "silent", False):
        config["ALICE_SILENT_MODE"] = True
    # Add more CLI overrides here if needed

    _config_cache = config
    return config

# Automatically load configuration when module is loaded
current_config = load_config()
