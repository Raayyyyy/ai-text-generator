from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app)
    app.config.from_object(Config)
    
    # 打印配置信息
    Config.print_config()
    
    from app.routes import generate
    app.register_blueprint(generate.bp)
    
    return app