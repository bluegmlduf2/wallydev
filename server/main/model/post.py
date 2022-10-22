from . import *

class Post(db.Model):
    """ 게시물 정보 취득 """
    __tablename__ = "post"

    postId = db.Column(db.String(255), primary_key=True)
    writerUid = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    imageUrl = db.Column(db.String(255))
    postViewCount = db.Column(db.Integer, nullable=False ,default=0)
    createdDate = db.Column(db.DateTime, nullable=False)
    updatedDate = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.postId = get_uuid() # 시스템의 현재시간과 호스트ID 기반으로 UUID 생성
        self.createdDate = get_current_time() # 작성시간 초기화
        self.updatedDate = get_current_time() # 수정시간 초기화

    def __repr__(self):
        return "<Post '{}'>".format(self.postId)