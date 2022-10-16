from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name
from flask.app import Flask

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

# 애플레이케이션 팩토리인 create_app을 사용하여 app변수의 중복적인 참조를 막는다(한번만 app변수를 만든다는 말)
def create_app(config_name: str) -> Flask:
    # 플라스크 앱 초기환경설정후 반환
    app = Flask(__name__) # 플라스크 app변수 생성
    app.config.from_object(config_by_name[config_name]) # 플라스크 실행모드 설정
    db.init_app(app) # 플라스크에 DB설정 등록
    flask_bcrypt.init_app(app)

    return app
