from . import *
from server.main.service.auth_helper import Auth
from server.main.service.user_service import get_user,save_user
from typing import Callable
import logging
import logging.handlers as handlers

def token_required(f) -> Callable:
    '''토큰에 유저정보가 존재 필수, uid반환'''
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data = Auth.check_verified_user(request)
            token = data.get('Authorization') # 인증여부
            uid =data.get('uid') # uid

            # 인증정보가 존재하지 않을 시 
            if not token:
                err_code=data.get('err_code') # 에러메세지코드
                return getMessage(err_code),401
            
            # 인증되었지만 DB에 유저정보가 없을시 DB에 유저ID 등록
            if not get_user(uid):
                save_user(uid)

            # 인증이 문제없으면 진행
            return f(uid ,*args, **kwargs)
        except Exception as e:
            # 로그 인스턴스 생성
            logger,uuid,user_ip = ceate_logger()
            loggerError,_,_ = ceate_logger(True)
            # 에러로그남기기
            logger.exception(f"[{user_ip}] [{uuid}] 에러 => ({e})")
            loggerError.exception(f"[{user_ip}] [{uuid}] 에러 => ({e})")
            return getMessage(770),401
    return decorated


def get_user_by_token(f) -> Callable:
    '''토큰에 유저정보가 존재 필수가아님, uid반환'''
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data = Auth.check_verified_user(request)
            uid =data.get('uid') # uid
            
            # 인증되었지만 DB에 유저정보가 없을시 DB에 유저ID 등록
            if uid:
                if not get_user(uid):
                    save_user(uid)

            # 인증이 문제없으면 진행
            return f(uid ,*args, **kwargs)
        except Exception as e:
            # 로그 인스턴스 생성
            logger,uuid,user_ip = ceate_logger()
            loggerError,_,_ = ceate_logger(True)
            # 에러로그남기기
            logger.exception(f"[{user_ip}] [{uuid}] 에러 => ({e})")
            loggerError.exception(f"[{user_ip}] [{uuid}] 에러 => ({e})")
            return getMessage(770),401
    return decorated


def ceate_logger(isErrorLog = False):
    '''로그 인스턴스 생성한다 파라미터정보(isErrorLog)에 따라 정보로그와 경고로그를 출력'''
    # 에러로그와 정보로그의 필요한 환경설정파일을 분리
    config = {
        'loggerName': 'errorLog' if isErrorLog else  'infoLog',
        'loggerPath': './log/logErrorfile.log' if isErrorLog else  './log/logfile.log',
    }

    # logger의 인스턴스 생성
    logger = logging.getLogger(config['loggerName'])
    
    # 로그고유번호용 UUID 8글자
    uuid=get_uuid()[:8]

    # 사용자 IP
    user_ip=request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)

    # 이미 logger인스턴스에 handlers가 등록된 경우 중복등록을 하지않음(로그중복호출방지)
    if len(logger.handlers) > 0:
        return logger,uuid,user_ip

    # 로그파일 출력설정 및 핸들러등록
    logger.setLevel(logging.INFO) # 로그설정 (INFO까지표시)
    logHandler = handlers.TimedRotatingFileHandler(config['loggerPath'], when='midnight', interval=1)
    logHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] | %(message)s '))
    logHandler.suffix = "%Y%m%d"
    logger.addHandler(logHandler)

    # 로그생성후 로그객체와 로그입력에 필요한 UUID와 IP를 반환한다
    return logger,uuid,user_ip


def exception_handler(f) -> Callable:
    '''에러핸들링'''
    @wraps(f)  # f.doc 과 같은 값을 잃어버리지 않도록 설정
    def decorated(*args, **kwargs):
        try:
            # 로그 인스턴스 생성
            logger,uuid,user_ip = ceate_logger()

            # 로그 기록
            logger.info(f"[{user_ip}] [{uuid}] 요청 => ({f.__qualname__})")
            result = f(*args, **kwargs)  # 인자로 전달받은 f 호출 / result는 f()의 반환값
            logger.info(f"[{user_ip}] [{uuid}] 응답 => ({f.__qualname__})")
        except UserError as e:
            # 사용자에러 처리
            logger.warning(f"[{user_ip}] [{uuid}] 예외 => ({e})")
            # 에러발생시 롤백
            db.session.rollback()
            return e.errorInfo,400
        except Exception as e:
            # 로그 인스턴스 생성
            loggerError,_,_ = ceate_logger(True)
            # 가터 애로 로그남기기
            logger.exception(f"[{user_ip}] [{uuid}] 에러 => ({e})")
            loggerError.exception(f"[{user_ip}] [{uuid}] 에러 => ({e})")
            # 에러발생시 롤백
            db.session.rollback()
            return getMessage(800),500
        else:
            # 성공적으로 반환된 값 전달
            return result
        finally:
            # 세션종료
            db.session.close()
    return decorated
