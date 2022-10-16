from typing import Dict, Tuple
from firebase_admin import auth # 파이어베이스 인증모듈

class Auth:

    @staticmethod
    def check_verified_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        '''인증 유저 확인 '''
        auth_token= data.headers.get('authorization')
        if auth_token:
            try:
                # 파이어베이스에서 유저정보인증 확인
                user = auth.verify_id_token(auth_token.replace("Bearer ",""))
                response_object = {
                    'status': 'success',
                    'message': '성공적으로 인증되었습니다',
                    'Authorization': True,
                    'uid': user.get('uid'),
                }
                return response_object
            except:
                #유효하지않은 토큰
                return {'err_code': 771}
        else:
            # 인증정보가 존재하지않을때
            return {'err_code': 772}



    @staticmethod
    def get_user_info(uid: str):
        '''파이어베이스에 저장된 유저의 정보을 반환한다'''
        try:
            user = auth.get_user(uid) # 유저정보취득
            
            # 유저 닉네임 (닉네임 존재하지않을시 생성타임스탬프를 이용해 유저닉네임생성) 삼항연산자
            nickname=not user.display_name and "USER" + str(user.user_metadata.creation_timestamp) or user.display_name
            
            # 전달할 유저정보
            userInfo = {
                'nickname':nickname,
                'user_image':user.photo_url
            }
            return userInfo
        except auth.UserNotFoundError:
            # 전달할 탈퇴유저정보
            return {
                'nickname':'탈퇴한 회원',
                'user_image':None
            }