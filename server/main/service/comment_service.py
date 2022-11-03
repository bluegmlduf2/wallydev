from . import *

def get_comment(uid,postId):
    '''댓글 정보 취득'''
    # 댓글 정보취득
    comment = db.session.query(Comment).\
        filter(Comment.postIdRef==postId).\
        order_by(Comment.createdDate).all()

    # 댓글 정보를 변환
    for c in comment:
        commentData=c # 댓글데이터

        # 댓글데이터
        comment_user = Auth.get_user_info(commentData.writerUid) # 파이어베이스에 저장된 유저정보 취득
        comment_user_auth = True if uid == commentData.writerUid else False #댓글 작성자 유무
        setattr(commentData,'writerUserName',comment_user['nickname']) # 댓글 작성자의 닉네임등록
        setattr(commentData,'commentUserAuth',comment_user_auth) # 댓글 작성자 유무

    return comment


def create_comment(uid,payload):
    '''댓글 등록'''
    try:
        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재하는 경우
        if user:
            comment = Comment()
            comment.postIdRef = payload['postId']
            comment.commentContent = payload['commentContent']
            comment.writerUid = user.uid
        
            db.session.add(comment)
            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '댓글을 등록했습니다'
            }
            return response_object, 201
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'등록된 댓글')


def update_comment(uid,payload):
    '''댓글 수정'''
    try:
        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            comment = Comment.query.filter_by(writerUid=uid, commentId=payload['commentId']).first()
            # 댓글존재여부체크
            if not comment:
                raise UserError(702,'댓글')

            comment.commentContent = payload['commentContent']

            db.session.add(comment)
            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '댓글을 수정했습니다'
            }
            return response_object, 201        
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'수정된 댓글')


def destroy_comment(uid,commentId):
    '''댓글 삭제'''
    try:

        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            Comment.query.filter_by(writerUid=uid, commentId=commentId).delete()

            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '댓글을 삭제했습니다'
            }
            return response_object, 201
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'삭제된 댓글')
