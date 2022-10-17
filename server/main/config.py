import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__)) # 현재있는 파일의 디렉토리 절대경로 (SQLite저장위치지정을위해)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False
    # 서버 이미지 저장용 URL (서버에서 이미지를 저장할때 사용하는 URL)
    SERVER_IMAGE_URL = os.getenv('SERVER_IMAGE_URL')
    # 게시물 이미지 임시 저장 경로와 저장된 게시물 저장경로
    POST_TEMP_FILE_PATH = basedir+'/image/posttempimage/'
    POST_FILE_PATH = basedir+'/image/postimage/'

class DevelopmentConfig(Config):
    # 개발환경에서 사용할 sqllite
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'wallydev_main.db') # 데이터베이스 접속주소, SQLite를 사용해서 db를 파일로 관리한다 
    SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy의 이벤트를 처리하는 옵션 (수정사항에 대한 TRACK)


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'wallydev_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # 실제 배포를 위한 DB설정 (.env파일에 값이 존재하지않을 경우 2번째 인자값을 기본값으로 사용)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={charset}'.format(**{
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'host': os.getenv('DB_HOST', 'localhost'),
        'db': os.getenv('DB_NAME', 'wallydev'),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
