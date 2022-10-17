# 서비스에서 공통으로 사용하는 모듈
from server.main import db
from server.main.model.post import Post
from server.main.model.user import User
from server.main.model.comment import Comment
from server.main.service.auth_helper import Auth
from server.main.util import UserError,get_current_time,sort_by_id,convert_string_to_date,moveImageFile
from sqlalchemy import exc,case
from datetime import datetime,timedelta

def remove_unnecessary_elements(selection):
    '''SQL의 조건 매개변수에 불필요한 칼럼을 제거한다'''
    # 검색조건으로 필요한 칼럼, 메인화면에서 검색시 체류일정은 검색조건으로 사용하지 않는다
    necessary_elements = ['country'] if selection.get('searchOnlyCountry',False) else ['country','stayStatus']
    # 값이 존재하고, 필요한 칼럼만 남겨서 검색을 위한 딕셔너리로 반환
    filters={k: v for k, v in selection.items() if v is not None and k in necessary_elements}
    return filters

def get_next_page(selection):
    # 페이지네이션 없이 일정만 가져오는 경우 모든 일정을 표시한다
    if selection is None:
        return 1
    # 모든일정의 초기화시 모든 일정을 표시한다
    elif selection.get('getAllPages',False):
        return 1
    else:
        # 다음페이지를 가져온다 만약 가져올 페이지가 존재하지 않으면 1페이지를 가져온다
        return selection['currentPage']+1 if selection.get('currentPage',False) else 1 

def get_per_page(selection):
    # 페이지네이션 없이 일정만 가져오는 경우 모든 일정을 표시한다
    if selection is None:
        return 10000
    # 모든일정의 초기화시 모든 일정을 표시한다
    elif selection.get('getAllPages',False):
        return 10000
    else:
    # 한 페이지에 표시할 게시물의 수를 취득, 존재하지 않을 경우 10개씩 표시한다
        return  20 if selection.get('get20perpage',False) else 10

def get_filter_condition_by_searchword(selection):
    '''제목과 내용에 해당 단어를 포함하는지에 대한 조건을 반환'''
    # 재검색어
    searchWord = selection.get('searchWord',None) if selection else None

    # 검색어가 존재할 경우
    if searchWord:
        # 재검색시 사용하는 검색조건 (제목과 내용에 해당 단어를 포함하는지 검색)
        search = "%{}%".format(searchWord)
        # 재검색의 검색조건 반환
        return (Post.title.like(search))|(Post.content.like(search))
    else:
    # 검색어가 존재하지않을 경우 (모든일정표시)
        return True