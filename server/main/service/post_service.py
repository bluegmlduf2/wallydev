from . import *
from server.main.service.comment_service import get_comment

def get_post(uid,postId):
    '''게시물 정보 취득'''

    # 게시물 관련
    post = Post.query.filter_by(postId=postId).first() # 게시물 정보 취득

    # 게시물존재여부체크
    if not post:
        raise UserError(702,'게시물')

    # 유저정보 관련
    user = Auth.get_user_info(post.writerUid) # 파이어베이스에 저장된 유저정보 취득
    userAuth = True # 게시물 작성자인 경우

    # 게시물 작성자가 아닌 경우나 로그인하지 않은 경우
    if uid != post.writerUid:
        userAuth = False # 게시물 작성자가 아닌 경우
        update_view_count(post) # 게시물의 조회수 증가
    
    setattr(post,'writerUserName',user['nickname']) # 게시물 작성자의 닉네임등록
    setattr(post,'userAuth',userAuth) # 게시물 작성자 유무

    # 댓글정보 취득
    comment = get_comment(uid,postId)
    setattr(post,'comment', comment)

    return post

def get_post_list(payload):
    '''게시물 리스트 정보 취득'''

    # 재검색시 사용하는 검색조건
    filterSearchWord = get_filter_condition_by_searchtext(payload)
    page=int(payload['page'])
    limit=int(payload['limit'])
    category=payload['category']

    # 내 할일일정의 상세 정보 취득
    postQuery = Post.query.filter_by(category=category).\
        filter(filterSearchWord).\
        order_by(Post.createdDate)

    postList = postQuery.paginate(page,limit,error_out=False).items # 할일일정의 페이지네이션 된 값

    return postList


def create_post(uid,payload):
    '''게시글 등록'''
    try:
        user=User.query.filter_by(uid=uid).first()

        # 등록된 유저가 있는지 확인
        if user:
            # 글내용의 이미지 url변경
            # filteredContent = payload['content'].replace(
            #     'api/image/temp/', 'api/image/post/')
            # payload['content'] = filteredContent

            # # 게시글의 임시 이미지 파일을 저장용 폴더에 이동
            # moveImageFile(payload['tempImages'])            
            
            # 등록할 게시물 정보입력
            post = Post()
            post.writerUid = uid
            post.title = payload['title']
            post.content = payload['content']
            post.category = payload['category']

            db.session.add(post)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': '게시글을 등록했습니다',
                'postId': post.postId,
                'category': post.category
            }
            return response_object, 201
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'등록된 게시물')


def update_post(uid,payload):
    '''게시글 수정'''
    try:
        user=User.query.filter_by(uid=uid).first()

        # 유저의 선택정보가 전부 입력되어있는지 확인
        if not user.country or not user.stayStatus:
            raise UserError(701,'유저의 국가/체류상태')

        # 기존 유저가 존재할 경우 유저선택정보를 갱신
        if user:
            # 화면에서 입력한 데이터
            inputData = payload['inputData']

            # 필수 입력정보가 전부 입력되어있는지 확인
            if (not inputData['postId'] 
            or not inputData['startDate'] 
            or not inputData['endDate'] 
            or not inputData['title'] 
            or not inputData['content'] 
            or not inputData['country'] 
            or not inputData['stayStatus']):
                raise UserError(701,'필수항목')

            # 제목의 입력글자수 체크
            if len(inputData['title'])>35:
                raise UserError(706,'35')

            # 국가선택에 지정한 값이외에 다른 값을 입력한 경우
            if inputData['country'] not in ['US','JP','CN']:
                raise UserError(704)

            # 체류상태에 지정한 값이외에 다른 값을 입력한 경우
            if inputData['stayStatus'] not in ['0','1','2']:
                raise UserError(704)

            # 일정 시작일이 종료일보다 큰 경우
            if inputData['startDate'] > inputData['endDate']:
                raise UserError(705)
       
            # 시간 데이터
            startDate = datetime.strptime(inputData['startDate'],'%Y-%m-%d') # 일정시작일
            endDate = datetime.strptime(inputData['endDate'],'%Y-%m-%d') # 일정종료일
            currentDate = datetime.strptime(get_current_time().strftime('%Y-%m-%d'),'%Y-%m-%d') # 현재시간
            # 나의 입국날짜 (만약존재하지 않을시 현재 날짜를 넣는다)
            entryDate = currentDate if user.entryDate is None else datetime.strptime(user.entryDate.strftime('%Y-%m-%d'),'%Y-%m-%d')
            afterEntryDate = (currentDate-entryDate).days # 내 입국후 경과 일수

            # 글내용의 이미지 url변경
            filteredContent = inputData['content'].replace(
                'api/image/temp/', 'api/image/post/')
            inputData['content'] = filteredContent

            # 게시글의 임시 이미지 파일을 저장용 폴더에 이동
            moveImageFile(inputData['tempImages'])       

            # 수정할 게시물 정보입력
            post = Post.query.filter_by(writerUid=uid, postId=inputData['postId']).first()
            # 게시물존재여부체크
            if not post:
                raise UserError(702,'게시물')

            post.title = inputData['title']
            post.content = inputData['content']
            post.country = inputData['country']
            post.stayStatus = inputData['stayStatus']
            post.afterEntryDate = afterEntryDate
            post.startDate = startDate
            post.endDate = endDate

            db.session.add(post)
            db.session.commit()
                        
            response_object = {
                'status': 'success',
                'message': '게시글을 수정했습니다',
                'postId': post.postId
            }
            return response_object, 201
    except exc.IntegrityError as e:
        # 이미 등록된 데이터가 존재할 경우
        raise UserError(703,'수정된 게시물')


def update_view_count(post):
    '''게시물의 조회수 증가'''
    post.postViewCount = post.postViewCount+1 
    db.session.commit()


def get_post_detail(postId,requestItem):
    """게시물에서 특정 정보만 취득"""
    # 필수 입력정보가 전부 입력되어있는지 확인
    if not postId or not requestItem:
        raise UserError(701,'필수항목')

    post_detail_column = [getattr(Post,attr) for attr in requestItem] # 취득할 데이터
    post_detail = Post.query.filter_by(postId=postId).\
        with_entities(*post_detail_column).first()
    return post_detail