import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# 預設設定值
DEFAULT_CONFIG = {
    "ALICE_MODEL": "default",
    "ALICE_DEVICE_TYPE": "macos",  # 指定運行設備類型
    "ALICE_LANGUAGE": "zh-TW",  # 指定代理的響應語言
    "ALICE_API_KEY": None, # "your-api-key-here"
    "ALICE_TIMEOUT": 30,
    "ALICE_RETRIES": 3,
    "ALICE_BASE_URL": "https://openrouter.ai/api/v1",
    "ALICE_LOG_LEVEL": "INFO",
    "ALICE_SILENT_MODE": False
}

_config_cache: Dict[str, Any] = None  # 用來快取設定


def load_config() -> Dict[str, Any]:
    """載入設定，優先順序: 1.本地.env 2.家目錄.env 3.環境變數 4.預設值"""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    config = DEFAULT_CONFIG.copy()

    # 1. 載入本地 .env (專案根目錄)
    local_env = Path(".env")
    if local_env.exists():
        load_dotenv(local_env)

    # 2. 載入家目錄 .env (~/.alice/.env)
    home_env = Path.home() / ".alice" / ".env"
    if home_env.exists():
        load_dotenv(home_env)

    # 3. 從環境變數更新設定
    for key in DEFAULT_CONFIG:
        env_value = os.getenv(key)
        if env_value is not None:
            # 特殊處理布林值設定
            if key == "ALICE_SILENT_MODE":
                config[key] = env_value.lower() in ("true", "1", "yes", "on", "y")
            else:
                config[key] = env_value

    _config_cache = config
    return config


# 模組載入時自動讀取設定
current_config = load_config()
