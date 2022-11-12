# 유틸에서 공통으로 사용하는 모듈
from flask import current_app,request,abort
from server.main import db
from sqlalchemy import case
from datetime import datetime
from PIL import Image, ExifTags  # 이미지 사이즈 변경
from functools import wraps
from pytz import timezone
import os # 파일 이동용
from uuid import uuid1
import shutil # 파일 이동용
import random # 디폴트 이미지명 난수생성

class UserError(Exception):
    '''사용자 에러 클래스'''
    # 인스턴스 생성시 리턴되는 인스턴스변수
    def __init__(self, errCode, param=None):
        self.errorInfo = getMessage(errCode, param)

    # 객체가 print함수에 호출될때 표시되는 함수
    def __str__(self):
        return self.errorInfo['message']

def getMessage(code, param=None):
    '''사용자 정의 에러메세지'''
    # 에러메세지
    MESSAGE = {
        # 400번대 에러메세지 
        700: param,
        701: f"{param}을 입력해주세요",
        702: f"등록되지 않은 {param}입니다",
        703: f"이미 {param}입니다",
        704: "유효하지 않은 선택정보입니다",
        705: "종료일이 시작일보다 이전 날짜여서는 안됩니다",
        706: f"입력가능한 글자수 {param}자를 초과했습니다",

        # 파일관련에러
        750: "파일명이 존재하지 않습니다 \n파일 업로드에 실패했습니다",
        751: "빈 파일입니다\n파일 업로드에 실패했습니다",
        752: "파일 사이즈를 확인해주세요\n파일 사이즈가 5MB이상인 경우에는 등록할수없습니다",
        753: "이미지 파일을 등록해주세요",

        # 권한관련에러
        770: "인증정보 처리중 에러가 발생했습니다",
        771: "유효하지않은 인증정보입니다\n다시 로그인해서 진행해주세요",
        772: "존재하지않는 인증정보입니다",
        
        # 500번대 에러메세지
        800: "예기치 못한 에러가 발생했습니다\n잠시후에 다시 시도해주세요",
    }

    # 해당 에러발생시 홈으로 이동할지 여부
    MOVE_TO_HOME=[ 702 ]

    return {
        "code": code,
        "message": MESSAGE[code],
        "moveToHome": code in MOVE_TO_HOME
    }

def get_uuid():
    '''UUID를 문자열로 취득'''
    return str(uuid1())

def get_current_time():
    '''서울기준으로 현재시간을 가져온다'''
    return datetime.now(timezone('Asia/Seoul'))

def sort_by_id(postIds):
    '''매개변수로 전달된 리스트의 순서를 postIds의 순서에 맞춰 변경한다'''
    # 순환참조 Post를 import시 발생하는 순환참조에러 방지를 위해 아래와같이 import (circular import)
    from server.main.model.post import Post
    
    # 사용자 정렬 (등록일순)
    if postIds:
        return case(
            {_id: index for index, _id in enumerate(postIds)},
            value=Post.postId
        )
    else:
        return None

def convert_string_to_date(inputDate):
    '''문자열을 데이터 형식(YYYY-MM-DD형식)으로 바꾼다'''
    # datetime.strptime(inputDate,"%Y-%m-%dT%H:%M:%S.%fZ").date().strftime("%Y-%m-%d")
    # 문자열 yyy-mm-dd'T'HH:mm:ss를 문자열 YYYY-MM-DD로 변환한 경우 
    format = '%Y-%m-%d' # YYYY-MM-DD형식
    return datetime.strptime(inputDate, format).date()

def upload_image(param):
    '''게시글 이미지 추가'''
    try:
        # 파일명변경
        time = get_current_time().strftime('%Y%m%d%H%M%S')  # 현재시간을 YYYYmmddHHMMSS 형태의 시간 출력
        ranNum = str(random.randint(1, 999999)).rjust(4, "0")  # 난수4자리,공백은0으로채움
        resize_image_fileNm = time+ranNum+".jpg"  # 변경후 저장한 파일명

        # 이미지 열기
        image = Image.open(param)
        
        # 이미지 너비가 넓을경우 90도 회전이 되는데 그걸 방지
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 

        try:
            exif = dict(image._getexif().items())
            # 사진을 촬영한 기기에 입력된 회전정보
            rotateInfo=exif.get('orientation',None)

            # 카메라나 스마트폰 카메라로 사진을 찍으면 JPEG 화상과 함게 기기 내의 중력센서를 이용한 회전 정보(3,6,8)가 EXIF 태그 중 하나로서 담긴다.
            if rotateInfo == 3 :
                image=image.rotate(180, expand=True)
            elif rotateInfo == 6 :
                image=image.rotate(270, expand=True)
            elif rotateInfo == 8 :
                image=image.rotate(90, expand=True)
        except AttributeError:
            # items()의 속성이 없는 경우 image를 회전하지않고 그대로 사용
            image=image
        
        # 이미지 저장
        source = current_app.config['POST_TEMP_FILE_PATH']+resize_image_fileNm  # 임시파일저장경로

        # RGB형식으로 변경후 , 이미지 파일 저장
        image.convert('RGB').save(source)  # resize사용시 image -> resize_image

        # 임시 저장된 이미지의 URL
        url = current_app.config['SERVER_IMAGE_URL']+'temp/'+resize_image_fileNm
    except IOError:
        # 파일형식이 이미지인가 체크
        raise UserError(753)
    except Exception as e:
        raise e
    else:
        return url,resize_image_fileNm


# 임시이미지 파일을 저장용 폴더에 이동
def moveImageFile(imageFileNames):
    # 파일 이동에 필요한 설정부분
    postTempFilePath = current_app.config['POST_TEMP_FILE_PATH'] # 게시물 임시 저장 위치
    postFilePath = current_app.config['POST_FILE_PATH'] # 게시물 저장 위치
    imageTempForder = os.listdir(postTempFilePath) # 임시파일이 위치한 폴더

    # 파일 이동 실행 부분
    for imageFile in imageTempForder:
        if imageFile in imageFileNames:
            shutil.move(postTempFilePath + imageFile, postFilePath + imageFile) # 파일이동