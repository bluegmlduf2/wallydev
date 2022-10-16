# wallydev
### VUE Terminal commands


```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

### SERVER Terminal commands
Note: make sure you have `pip` and `virtualenv` installed.

    Initial installation: make install

    To run test: make tests

    To run application: make run

    To run all commands at once : make all

Make sure to run the initial migration commands to update the database. (디비초기설정시 venv환경에서 실시)
    
    > python3 manage.py db init # DB 초기화 , 1.최초 한번만 실행 2.migrate폴더생성

    > python3 manage.py db migrate # 모델을 리비전으로 만들어서 migrate폴더에 저장

    > python3 manage.py db migrate --message 'initial database migration' # 모델을 리비전으로 만들어서 migrate폴더에 저장 (옵션은 리비전 명)

    > python3 manage.py db upgrade  # 현재 리비전을 migrate로 생성한 신규 리비전으로 변경 

    0.해당 명령어를 사용하기 위해선 venv환경이여야한다
    1.프로젝트 최초에 db init
    2.model수정시 migrate후 리비전 생성
    3.기존 사용하던 리비전을 2에서 생성한 신규 리비전으로 변경 
    4.model을 수정하면 migrate와 upgrade를 실행해줘야함

    리비전 오류가 발생할시, 가장 최근의 리비전으로 이동후 업그레이드
    0. python3 manage.py db stamp head
    1. python3 manage.py db migrate 
    2. python3 manage.py db upgrade  

    기타
    - 만약 변경사항이 적용이 안된다면 테이블을 지웠다가 upgrade를 해본다
    - 테이블 추가후 해당 추가한 model을 로직에서 사용하는 부분이 없으면 테이블 추가가 안된다

    기타명령어
    1.python3 manage.py db help 명령어보기
    2.python3 manage.py db upgrade 리비전명 리비전업그레이드
    3.python3 manage.py db downgrade 리비전명 리비전다운그레이드
    4.python3 manage.py db history 리비전히스토리열람
