from . import *
from server.main.util.dto import CommentReplyDto
from server.main.service.comment_reply_service import create_comment_reply,update_comment_reply,destroy_comment_reply

api = CommentReplyDto.api

@api.route('/<param>')
@api.param('param', '댓글번호/대댓글번호')
class CommentReply(Resource):
    @token_required
    @exception_handler
    @api.doc('대댓글 등록하기')
    def post(uid,self,param):
        """대댓글 정보를 등록"""
        payload = request.json
        return create_comment_reply(uid,payload)

    @token_required
    @exception_handler
    @api.doc('대댓글 수정하기')
    def put(uid,self,param):
        """대댓글 정보를 수정"""
        payload = request.json
        return update_comment_reply(uid,payload)

    @token_required
    @exception_handler
    @api.doc('대댓글 삭제하기')
    def delete(uid,self,param):
        """대댓글 정보를 삭제"""
        return destroy_comment_reply(uid,param)