from . import *

class CommentReply(db.Model):
    """ 게시물의 대댓글정보 """
    __tablename__ = "commentreply"

    commentReplyId = db.Column(db.String(255), primary_key=True,unique=True,nullable=False)
    commentReplyRefId = db.Column(db.String(255), ForeignKey('comment.commentId'),nullable=False) # comment 테이블의 외래키
    commentReplyUid = db.Column(db.String(255), primary_key=True,nullable=False)
    commentReplyContent = db.Column(db.Text(), nullable=True)
    commentReplyAddedDate = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.commentReplyId = get_uuid() # 시스템의 현재시간과 호스트ID 기반으로 UUID 생성
        self.commentReplyAddedDate = get_current_time() # 대댓글 등록수정시간 초기화

    def __repr__(self):
        return "<CommentReply '{}'>".format(self.uid)
