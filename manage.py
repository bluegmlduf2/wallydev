import os
import unittest

from flask_migrate import Migrate, MigrateCommand # 테이블을 생성하고 컬럼을 추가하는 등의 작업을 할 수 있게 해주는 Flask-Migrate 라이브러리
from flask_script import Manager
from flask_cors import CORS

from server import blueprint
from server.main import create_app, db

# main디렉토리에 있는 사용자 환경설정 끝난 플라스크 앱 초기화
app = create_app(os.getenv('SERVER_ENV') or 'dev') # dev, prod, test 중에 동작 (기본 dev)
app.register_blueprint(blueprint) # 플라스크 app객체로 app폴더의 blueprint을 등록
app.app_context().push()

# 해당 URL의 요청에 대해 CORS 허용
CORS(app,origins=[os.getenv('SERVER_FRONT_URL')])

# flask_script사용 등록
# 파이선 스크립트 실행 명령어등을 사용자 지정가능
# @manager.command def run() -> manager.run() -> python3 manage.py run
manager = Manager(app) 

migrate = Migrate(app, db, render_as_batch=True) # 컬럼타입변경시  migrate가 컬럼 타입을 변경할수있도록 설정 render_as_batch=True

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    # 플라스크 앱 기동
    app.run(port=5001)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('server/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
