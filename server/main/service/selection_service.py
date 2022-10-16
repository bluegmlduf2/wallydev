from . import *
from server.main.service.todo_list_service import get_my_todolist
from server.main.service.complete_list_service import get_my_completelist

def get_a_selection(uid):
    '''유저선택정보를 취득'''
    user=User.query.filter_by(uid=uid).first()
    todolist=get_my_todolist(uid)  # 내 할일일정 정보 취득
    completelist=get_my_completelist(uid)  # 내 완료일정 정보 취득
    setattr(user,'myTodolist',todolist['my_todolist']) # 내 할일일정 정보에서 일정 취득후 등록
    setattr(user,'myCompletelist',completelist['my_completelist']) # 내 완료일정 정보에서 일정 취득후 등록
    setattr(user,'todolistCount',todolist['total_count']) # 나의 총 할일 일정 취득후 등록
    setattr(user,'completelistCount',completelist['total_count']) # 나의 총 완료 일정 취득후 등록
    return user


def update_a_selection(uid,selection):
    '''유저선택정보를 갱신'''

    # 국가선택에 지정한 값이외에 다른 값을 입력한 경우
    if selection['country'] and selection['country'] not in ['US','JP','CN']:
        raise UserError(704)

    # 체류상태에 지정한 값이외에 다른 값을 입력한 경우
    if selection['stayStatus'] and selection['stayStatus'] not in ['0','1','2']:
        raise UserError(704)

    user=User.query.filter_by(uid=uid).first()
    # 기존 유저가 존재할 경우 유저선택정보를 갱신
    if user:
        user.country=selection['country']
        user.entryDate=datetime.strptime(selection['entryDate'], '%Y-%m-%d') if selection['entryDate'] else None
        user.stayStatus=selection['stayStatus']
        db.session.commit()
                    
        response_object = {
            'status': 'success',
            'message': '유저선택정보를 변경했습니다'
        }
        return response_object, 201