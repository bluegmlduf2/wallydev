from . import *
from server.main.util.dto import MyListDto
from server.main.service.my_list_service import get_mylist

api = MyListDto.api
_mylist = MyListDto.mylist

@api.route('/<param>')
@api.param('param', '유저가 작성한 일정')
class MyList(Resource):
    @token_required
    @exception_handler
    @api.doc('유저가 작성한 일정 가져오기')
    @api.marshal_list_with(_mylist, envelope='data')
    def get(uid,self,param):
        """유저가 작성한 일정을 반환"""
        selection = json.loads(param) #유저의 선택정보
        return get_mylist(uid,selection)