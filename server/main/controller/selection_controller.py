from . import *
from server.main.util.dto import SelectionDto
from server.main.service.selection_service import get_a_selection, update_a_selection

api = SelectionDto.api
_selection = SelectionDto.selection

@api.route('/selection')
class Selection(Resource):
    @token_required
    @exception_handler
    @api.doc('로그인한 유저의 선택사항을 취득')
    @api.marshal_list_with(_selection, envelope='data')
    def get(uid, self):
        """유저의 선택사항을 가져옴"""
        return get_a_selection(uid)
    
    @token_required
    @exception_handler
    @api.doc('로그인한 유저의 선택사항을 갱신')
    def put(uid, self):
        """유저의 선택사항을 갱신함"""
        payload = request.json
        return update_a_selection(uid, payload)