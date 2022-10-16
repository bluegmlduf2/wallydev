from . import *

def create_comment_reply(uid,param):
    '''대댓글 등록'''
    try:
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param['commentReplyContent'] or not param['commentId']:
            raise UserError(701,'필수항목')
        # 대댓글의 입력글자수 체크
        if len(param['commentReplyContent'])>1000:
            raise UserError(706,'1000')
        
        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            comment_reply = CommentReply()
            comment_reply.commentReplyContent = param['commentReplyContent']
            comment_reply.commentReplyRefId = param['commentId']
            comment_reply.commentReplyUid = uid

            db.session.add(comment_reply)
            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '대댓글을 등록했습니다'
            }
            return response_object, 201
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'등록된 대댓글')


def update_comment_reply(uid,param):
    '''대댓글 수정'''
    try:
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param['commentReplyContent'] or not param['commentReplyId']:
            raise UserError(701,'필수항목')
        # 대댓글의 입력글자수 체크
        if len(param['commentReplyContent'])>1000:
            raise UserError(706,'1000')

        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            comment_reply = CommentReply.query.filter_by(commentReplyUid=uid, commentReplyId=param['commentReplyId']).first()
            # 대댓글존재여부체크
            if not comment_reply:
                raise UserError(702,'대댓글')

            comment_reply.commentReplyContent = param['commentReplyContent']

            db.session.add(comment_reply)
            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '대댓글을 수정했습니다'
            }
            return response_object, 201        
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'수정된 대댓글')


def destroy_comment_reply(uid,commentReplyId):
    '''대댓글 삭제'''
    try:
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not commentReplyId:
            raise UserError(701,'필수항목')

        user=User.query.filter_by(uid=uid).first()
        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            CommentReply.query.filter_by(commentReplyUid=uid, commentReplyId=commentReplyId).delete()

            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '대댓글을 삭제했습니다'
            }
            return response_object, 201
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'삭제된 대댓글')