# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LLM配置
    API_KEY = os.getenv("API_KEY", "")  # 真实 key 请写在 .env，勿硬编码
    BASE_URL = os.getenv("BASE_URL", "https://ai.gitee.com/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "Qwen2.5-72B-Instruct") #Qwen2.5-72B-Instruct
    
    # 数据库配置（可选）
    DB_PATH = os.getenv("DB_PATH", "./data/recipes.db")
    
    # 应用配置
    APP_NAME = "曦曦饮食助手"
    VERSION = "1.0.0"