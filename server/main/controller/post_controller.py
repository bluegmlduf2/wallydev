from . import *
from server.main.util.dto import PostDto
from server.main.service.post_service import get_post,get_post_detail,create_post,update_post

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
    def get(uid,self,param):
        """게시물 정보를 반환"""
        return get_post(uid,param)

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


@api.route('/<param>/postdetail')
@api.param('param', '게시물 번호')
class PostDetail(Resource):
    @exception_handler
    @api.doc('게시물의 선택정보 가져오기')
    @api.marshal_with(_post, envelope='data')
    def post(self,param):
        """게시물에서 특정 정보만 취득"""
        payload = request.json
        return get_post_detail(param,payload)