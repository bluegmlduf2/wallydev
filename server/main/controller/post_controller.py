from . import *
from server.main.util.dto import PostDto
from server.main.service.post_service import get_post,get_post_list,create_post,update_post

api = PostDto.api
_post = PostDto.post


@api.route('')
class Post(Resource):
    @get_user_by_token
    @exception_handler
    @api.doc('게시물 가져오기')
    @api.marshal_list_with(_post, envelope='data')
    def get(uid,self):
        """게시물 정보를 취득"""
        payload = request.args.to_dict()
    
        # 필수 입력정보가 전부 입력되어있는지 확인
        if not payload.get('postId',False):
            raise UserError(701,'필수항목')

        return get_post(uid,payload)

    @token_required
    @exception_handler
    @api.doc('게시물 등록')
    @api.marshal_list_with(_post, envelope='data')
    def post(uid,self):
        """게시물 정보를 등록"""
        payload = request.json
        return create_post(uid,payload)

    @token_required
    @exception_handler
    @api.doc('게시물 수정')
    @api.marshal_list_with(_post, envelope='data')
    def put(uid,self):
        """게시물 정보를 수정"""
        payload = request.json
        return update_post(uid,payload)

@api.route('/postlist')
class PostList(Resource):
    @exception_handler
    @api.doc('게시물 리스트 취득')
    @api.marshal_list_with(_post, envelope='data')
    def get(self):
        """게시물 리스트 정보를 반환"""
        payload = request.args.to_dict()

        # 필수 입력정보가 전부 입력되어있는지 확인
        if not payload.get('page',False):
            raise UserError(701,'시작페이지')

        if not payload.get('limit',False):
            raise UserError(701,'종료페이지')

        if not payload.get('category',False):
            raise UserError(701,'카테고리')

        # 게시물 리스트 취득
        return get_post_list(payload)