from . import *

class Comment(db.Model):
    """ 게시물의 댓글정보 """
    __tablename__ = "comment"

    commentId = db.Column(db.String(255), primary_key=True,unique=True,nullable=False)
    postIdRef = db.Column(db.String(255), primary_key=True,nullable=False)
    commentUid = db.Column(db.String(255), primary_key=True,nullable=False)
    commentContent = db.Column(db.Text(), nullable=False)
    commentAddedDate = db.Column(db.DateTime, nullable=False)
    commentReply = relationship("CommentReply",order_by="CommentReply.commentReplyAddedDate",backref='Comment')

    def __init__(self):
        self.commentId = get_uuid() # 시스템의 현재시간과 호스트ID 기반으로 UUID 생성
        self.commentAddedDate = get_current_time() # 댓글 등록수정시간 초기화

    def __repr__(self):
        return "<Comment '{}'>".format(self.uid)
