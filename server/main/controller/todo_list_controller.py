from . import *
from server.main.util.dto import TodoListDto
from server.main.service.todo_list_service import get_my_todolist,update_todolist,destroy_todolist

api = TodoListDto.api
_todolist = TodoListDto.todolist

@api.route('')
@api.route('/<param>')
@api.param('param', '할일 일정 리스트')
class TodoList(Resource):
    @get_user_by_token
    @exception_handler
    @api.doc('할일 일정 가져오기')
    @api.marshal_list_with(_todolist, envelope='data')
    def post(uid,self):
        """할일 일정을 반환"""
        payload = request.json #유저의 선택정보
        return get_my_todolist(uid,payload)

    @token_required
    @exception_handler
    @api.doc('로그인한 유저의 할일일정을 추가')
    def put(uid,self,param):
        """유저의 할일일정을 추가함"""
        postId = param # 유저가 추가한 추천일정
        return update_todolist(uid,postId)

    @token_required
    @exception_handler
    @api.doc('로그인한 유저의 할일일정을 삭제')
    def delete(uid,self,param):
        """유저의 할일일정을 삭제함"""
        postId = param # 유저가 삭제한 추천일정
        return destroy_todolist(uid,postId)