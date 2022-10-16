from . import *

def get_mylist(uid,postInfo):
    '''유저가 작성한 일정 리스트 취득'''
    # 페이지네이션 취득
    page = get_next_page(postInfo) # 표시할 페이지수를 취득
    per_page = get_per_page(postInfo) # 한 페이지에 표시할 게시물의 수를 취득

    # 메인 SQL
    main_query = List.query.filter_by(writerUid=uid)

    # 재검색시 사용하는 검색조건
    filter_searchWord = get_filter_condition_by_searchword(postInfo)

    # 내 작성한 일정의 상세 정보 취득
    my_list_query = main_query.\
        filter(filter_searchWord).\
        order_by(List.createdDate.desc())

    # 서버에 저장된 내가 작성한 일정 취득
    my_list_count = main_query.count() # 내가 작성한 일정의 총 수
    my_list_result = my_list_query.paginate(page,per_page,error_out=False) # 나의 일정의 페이지네이션 된 값
    
    my_list = {
        'my_list':my_list_result.items, # 내가 작성한 일정
        'has_next':my_list_result.has_next, # 다음페이지 유무
        'current_page':my_list_result.page, # 현재페이지
        'total_count':my_list_count, # 총 작성일정 수
    }

    return my_list