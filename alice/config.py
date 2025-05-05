import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# 預設設定值
DEFAULT_CONFIG = {
    "ALICE_MODEL": "default",
    "ALICE_API_KEY": None, # "your-api-key-here"
    "ALICE_TIMEOUT": 30,
    "ALICE_RETRIES": 3,
    "ALICE_BASE_URL": "https://openrouter.ai/api/v1"
}

def load_config() -> Dict[str, Any]:
    """載入設定，優先順序: 1.本地.env 2.家目錄.env 3.環境變數 4.預設值"""
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
        # 檢查新舊格式的環境變數名稱
        env_value = os.getenv(key)
        if env_value is not None:
            config[key] = env_value

    return config

# 模組載入時自動讀取設定
current_config = load_config()
