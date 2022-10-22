from . import *

class Comment(db.Model):
    """ 게시물의 댓글정보 """
    __tablename__ = "comment"

    commentId = db.Column(db.String(255), primary_key=True,unique=True,nullable=False)
    postIdRef = db.Column(db.String(255), primary_key=True,nullable=False)
    writerUid = db.Column(db.String(255), primary_key=True,nullable=False)
    commentContent = db.Column(db.Text(), nullable=False)
    createdDate = db.Column(db.DateTime, nullable=False)
    updatedDate = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.commentId = get_uuid() # 시스템의 현재시간과 호스트ID 기반으로 UUID 생성
        self.createdDate = get_current_time() # 댓글 등록시간 초기화
        self.updatedDate = get_current_time() # 댓글 수정시간 초기화

    def __repr__(self):
        return "<Comment '{}'>".format(self.uid)
