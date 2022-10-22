from flask_restx import Api # REST API구현
from flask import Blueprint

from .main.controller.post_controller import api as post_ns
from .main.controller.image_controller import api as image_ns
from .main.controller.comment_controller import api as comment_ns

import firebase_admin # 서버 파 파이어베이스 모듈
from firebase_admin import credentials # 파이어베이스 초기화모듈


blueprint = Blueprint('api_wallydev', __name__) # __name__는 현재 모듈이다. 여기선 디렉토리 app이다. 이것을 Bluepirnt에 등록

# 파이어베이스 초기화 
cred = credentials.Certificate('wallydev-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

# flask_restx
# flask-restful의 라이브러리
# Swagger라는 rest api를 문서화해주는 도구를 지원
api = Api(
    blueprint, # flask_restx로 blueprint를 사용가능하도록 설정
    title='FLASK RESTPLUS(RESTX) API OF WALLYDEV',
    version='1.0',
    description='WALLYDEV for flask restplus (restx) web service',
    security='apikey'
)

api.add_namespace(post_ns, path='/api_wallydev/post')
api.add_namespace(post_ns, path='/api_wallydev/post/postlist')
api.add_namespace(comment_ns, path='/api_wallydev/comment')
api.add_namespace(image_ns, path='/api_wallydev/image')