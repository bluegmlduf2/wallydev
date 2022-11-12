from . import *
from server.main.util.dto import PostDto
from server.main.service.post_service import get_post, get_post_list, create_post, update_post, delete_post

api = PostDto.api
_post = PostDto.post


@api.route('')
@api.route('/<param>')
@api.param('param', '게시물 번호')
class Post(Resource):
    @get_user_by_token
    @exception_handler
    @api.doc('게시물 가져오기')
    @api.marshal_list_with(_post, envelope='data')
    def get(uid, self, param):
        """게시물 정보를 취득"""
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param:
            raise UserError(701, '필수항목')

        return get_post(uid, param)

    @token_required
    @exception_handler
    @api.doc('게시물 등록')
    @api.marshal_list_with(_post, envelope='data')
    def post(uid, self):
        """게시물 정보를 등록"""
        # 필수 입력정보가 전부 입력되어있는지 확인
        payload = request.json
        if not payload['title']:
            raise UserError(701, '타이틀')

        # 제목의 입력글자수 체크 (3글자)
        if len(payload['title']) > 35:
            raise UserError(706, '35')

        if not payload['category']:
            raise UserError(701, '카테고리')

        # 등록되지 않은 카테고리를 등록할 경우
        if payload['category'] not in ['today', 'food', 'javascript', 'vuejs']:
            raise UserError(704)

        if not payload['content']:
            raise UserError(701, '작성내용')

        return create_post(uid, payload)

    @token_required
    @exception_handler
    @api.doc('게시물 수정')
    @api.marshal_list_with(_post, envelope='data')
    def put(uid, self):
        """게시물 정보를 수정"""
        # 필수 입력정보가 전부 입력되어있는지 확인
        payload = request.json
        if not payload['postId']:
            raise UserError(702, '게시글')

        if not payload['title']:
            raise UserError(701, '타이틀')

        # 제목의 입력글자수 체크 (3글자)
        if len(payload['title']) > 35:
            raise UserError(706, '35')

        if not payload['category']:
            raise UserError(701, '카테고리')

        # 등록되지 않은 카테고리를 등록할 경우
        if payload['category'] not in ['today', 'food', 'javascript', 'vuejs']:
            raise UserError(704)

        if not payload['content']:
            raise UserError(701, '작성내용')

        return update_post(uid, payload)

    @token_required
    @exception_handler
    @api.doc('게시물 삭제')
    @api.marshal_list_with(_post, envelope='data')
    def delete(uid, self, param):
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not param:
            raise UserError(701, '필수항목')
        """게시물 정보를 삭제"""
        return delete_post(uid, param)


@api.route('/postlist')
class PostList(Resource):
    @exception_handler
    @api.doc('게시물 리스트 취득')
    @api.marshal_list_with(_post, envelope='data')
    def get(self):
        """게시물 리스트 정보를 반환"""
        payload = request.args.to_dict()

        # 필수 입력정보가 전부 입력되어있는지 확인
        if not payload.get('page', False):
            raise UserError(701, '시작페이지')

        if not payload.get('limit', False):
            raise UserError(701, '종료페이지')

        # 게시물 리스트 취득
        return get_post_list(payload)
