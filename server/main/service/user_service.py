from . import *

def get_user(uid):
    '''유저가 존재하는지 확인'''
    # 유저가 존재하면 1(True)를 반환함
    is_user=User.query.filter_by(uid=uid).count()
    return is_user

def save_user(uid):
    '''유저가 존재하지 않으면 DB에 유저 등록'''
    user = User()
    user.uid = uid
    db.session.add(user)
    db.session.commit()

