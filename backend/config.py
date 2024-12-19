import os
from dotenv import load_dotenv

# 确保加载 .env 文件
load_dotenv(override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE')
    
    # 打印配置信息用于调试
    @classmethod
    def print_config(cls):
        print("=== Configuration ===")
        print(f"OPENAI_API_KEY configured: {'Yes' if cls.OPENAI_API_KEY else 'No'}")
        print(f"OPENAI_API_BASE: {cls.OPENAI_API_BASE}")
        print("==================")