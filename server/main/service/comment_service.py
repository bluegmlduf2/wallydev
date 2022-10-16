from . import *

def get_comment(uid,postId):
    '''댓글 정보 취득'''
    # 필수 입력정보가 전부 입력되어있는지 확인
    if not postId:
        raise UserError(701,'필수항목')

    # 댓글과 대댓글 정보취득
    comment = db.session.query(Comment).\
        outerjoin(CommentReply,Comment.commentId == CommentReply.commentReplyRefId).\
        filter(Comment.postIdRef==postId).\
        order_by(Comment.commentAddedDate).all()

        # 댓글과 대댓글의 정보를 변환
    for c in comment:
        commentData=c # 댓글데이터
        commentReplyData=c.commentReply # 대댓글데이터

        # 댓글데이터
        comment_user = Auth.get_user_info(commentData.commentUid) # 파이어베이스에 저장된 유저정보 취득
        comment_user_auth = True if uid == commentData.commentUid else False #댓글 작성자 유무
        setattr(commentData,'commentUserName',comment_user['nickname']) # 댓글 작성자의 닉네임등록
        setattr(commentData,'commentUserImage',comment_user['user_image']) # 댓글 작성자의 이미지 url
        setattr(commentData,'commentUserAuth',comment_user_auth) # 댓글 작성자 유무

        # 대댓글데이터
        if commentReplyData:
            for commentReply in commentReplyData:
                comment_reply_user = Auth.get_user_info(commentReply.commentReplyUid) # 파이어베이스에 저장된 유저정보 취득
                comment_user_reply_auth = True if uid == commentReply.commentReplyUid else False #대댓글 작성자 유무
                setattr(commentReply,'commentReplyUserName',comment_reply_user['nickname']) # 대댓글 작성자의 닉네임등록
                setattr(commentReply,'commentReplyUserImage',comment_reply_user['user_image']) # 대댓글 작성자의 이미지 url
                setattr(commentReply,'commentReplyUserAuth',comment_user_reply_auth) # 대댓글 작성자 유무

    return comment


def create_comment(uid,param):
    '''댓글 등록'''
    try:
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param['commentContent']:
            raise UserError(701,'필수항목')

        # 댓글의 입력글자수 체크
        if len(param['commentContent'])>1000:
            raise UserError(706,'1000')

        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            comment = Comment()
            comment.commentContent = param['commentContent']
            comment.postIdRef = param['postId']
            comment.commentUid = uid

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


def update_comment(uid,param):
    '''댓글 수정'''
    try:
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param['commentContent'] or not param['commentId']:
            raise UserError(701,'필수항목')

        # 댓글의 입력글자수 체크
        if len(param['commentContent'])>1000:
            raise UserError(706,'1000')

        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            comment = Comment.query.filter_by(commentUid=uid, commentId=param['commentId']).first()
            # 댓글존재여부체크
            if not comment:
                raise UserError(702,'댓글')

            comment.commentContent = param['commentContent']

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
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not commentId:
            raise UserError(701,'필수항목')

        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            comment_reply = CommentReply.query.filter_by(commentReplyRefId=commentId).count()
            # 대댓글이 존재하지 않는 댓글만 삭제가능
            if not comment_reply:
                Comment.query.filter_by(commentUid=uid, commentId=commentId).delete()

                db.session.commit()
                            
                response_object = {
                    'status': 'success',
                    'message': '댓글을 삭제했습니다'
                }
                return response_object, 201
            else:
                raise UserError(700,'대댓글이 존재하므로 삭제할수없습니다')
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'삭제된 댓글')
