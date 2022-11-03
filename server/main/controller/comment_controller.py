from . import *
from server.main.util.dto import CommentDto
from server.main.service.comment_service import create_comment, update_comment, destroy_comment

api = CommentDto.api
_comment = CommentDto.comment


@api.route('')
@api.route('/<param>')
class Comment(Resource):

    @token_required
    @exception_handler
    @api.doc('댓글 등록하기')
    def post(uid, self):
        """댓글 정보를 등록"""
        payload = request.json

        # 필수 입력정보가 전부 입력되어있는지 확인
        if not payload['commentContent']:
            raise UserError(701, '필수항목')

        # 댓글의 입력글자수 체크
        if len(payload['commentContent']) > 1000:
            raise UserError(706, '1000')

        return create_comment(uid, payload)

    @token_required
    @exception_handler
    @api.doc('댓글 수정하기')
    def put(uid, self):
        """댓글 정보를 수정"""
        payload = request.json

        # 필수 입력정보가 전부 입력되어있는지 확인
        if not payload['commentId']:
            raise UserError(701, '필수항목')

        if not payload['commentContent']:
            raise UserError(701, '필수항목')

        # 댓글의 입력글자수 체크
        if len(payload['commentContent']) > 1000:
            raise UserError(706, '1000')

        return update_comment(uid, payload)

    @token_required
    @exception_handler
    @api.doc('댓글 삭제하기')
    def delete(uid, self, param):
        """댓글 정보를 삭제"""

        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param:
            raise UserError(701, '필수항목')

        return destroy_comment(uid, param)
