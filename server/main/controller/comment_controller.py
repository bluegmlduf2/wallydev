from . import *
from server.main.util.dto import CommentDto
from server.main.service.comment_service import get_comment,create_comment,update_comment,destroy_comment

api = CommentDto.api
_comment = CommentDto.comment

@api.route('/<param>')
@api.param('param', '게시물 번호/댓글번호')
class Comment(Resource):
    @get_user_by_token
    @exception_handler
    @api.doc('댓글 가져오기')
    @api.marshal_list_with(_comment, envelope='data')
    def get(uid,self,param):
        """댓글 정보를 반환"""
        return get_comment(uid,param)

    @token_required
    @exception_handler
    @api.doc('댓글 등록하기')
    def post(uid,self,param):
        """댓글 정보를 등록"""
        payload = request.json
        return create_comment(uid,payload)

    @token_required
    @exception_handler
    @api.doc('댓글 수정하기')
    def put(uid,self,param):
        """댓글 정보를 수정"""
        payload = request.json
        return update_comment(uid,payload)

    @token_required
    @exception_handler
    @api.doc('댓글 삭제하기')
    def delete(uid,self,param):
        """댓글 정보를 삭제"""
        return destroy_comment(uid,param)