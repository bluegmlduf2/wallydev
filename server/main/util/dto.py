from flask_restx import Namespace, fields


class PostDto:
    api = Namespace('post', description='게시물정보')
    commentSchema = api.model('commentSchema', {
        'commentId': fields.String(description='댓글 ID'),
        'commentUserName': fields.String(description='댓글 작성자'),
        'commentContent': fields.String(description='댓글 내용'),
        'commentAddedDate': fields.Date(description='댓글 작성일'),
        'commentUserAuth': fields.Boolean(description='댓글작성자유무'),
        'isOpenClicked': fields.Boolean(description='댓글 열기닫기버튼 활성화유무',default=False),
        'isCommentClicked': fields.Boolean(description='댓글 수정버튼 활성화유무',default=False),
        'isWriteClicked': fields.Boolean(description='댓글 댓글작성버튼 활성화유무',default=False),
    })# 댓글의 스키마
    post = api.model('post', {
        'postId': fields.String(description='게시물 번호'),
        'writerUserName': fields.String(description='게시물 작성자'),
        'title': fields.String(description='게시물 제목'),
        'content': fields.String(description='게시물 내용'),
        'country': fields.String(description='선택국가'),
        'stayStatus': fields.String(description='체류상태'),
        'isAdded': fields.Boolean(description='추가된 일정 유무'),
        'isCompleted': fields.Boolean(description='완료된 일정 유무'),
        'postViewCount': fields.Integer(description='조회수'),
        'afterEntryDate': fields.Integer(description='입국경과일'),
        'startDate': fields.Date(description='일정시작일'),
        'endDate': fields.Date(description='일정종료일'),
        'createdDate': fields.Date(description='게시글작성일'),
        'userAuth': fields.Boolean(description='게시글작성자유무'),
        'myStartDate': fields.Date(description='나의 일정 시작일'),
        'myEndDate': fields.Date(description='나의 일정 종료일'),
        'comment' :fields.List(description='댓글정보', default=[], cls_or_instance=fields.Nested(commentSchema)),
    })
class ImageDto:
    api = Namespace('image', description='이미지 정보')
    image = api.model('post', {
        'imagefileName': fields.String(description='등록한 이미지의 파일명'),
        'imageUrl': fields.String(description='등록한 이미지의 URL'),
    })

class CommentDto:
    api = Namespace('comment', description='댓글정보')
    comment = api.model('comment', {
        'commentId': fields.String(description='댓글 ID'),
        'commentUserName': fields.String(description='댓글 작성자'),
        'commentContent': fields.String(description='댓글 내용'),
        'commentAddedDate': fields.Date(description='댓글 작성일'),
        'commentUserAuth': fields.Boolean(description='댓글작성자유무'),
        'isOpenClicked': fields.Boolean(description='댓글 열기닫기버튼 활성화유무',default=False),
        'isCommentClicked': fields.Boolean(description='댓글 수정버튼 활성화유무',default=False),
        'isWriteClicked': fields.Boolean(description='댓글 댓글작성버튼 활성화유무',default=False),
    })# 댓글의 스키마