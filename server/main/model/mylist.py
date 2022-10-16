from . import *

class Mylist(db.Model):
    """ 유저가 선택중인 일정 정보 취득 """
    __tablename__ = "mylist"

    myListId = db.Column(db.String(255), unique=True,nullable=False) # 다른 list 테이블의 외래키
    myListIdRef = db.Column(db.String(255), primary_key=True,nullable=False) # 다른 list 테이블의 외래키
    uid = db.Column(db.String(255), primary_key=True,nullable=False)
    listKind = db.Column(db.String(8), nullable=False) # todo,rec,all,complete
    addedDate = db.Column(db.DateTime, nullable=False)
    myStartDate = db.Column(db.Date)
    myEndDate = db.Column(db.Date)

    def __init__(self):
        self.myListId = get_uuid() # 시스템의 현재시간과 호스트ID 기반으로 UUID 생성
        self.addedDate = get_current_time() # 일정 등록시간 초기화

    def __repr__(self):
        return "<Mylist '{}'>".format(self.uid)
