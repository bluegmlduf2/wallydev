# 맥은 기본 python버전 2.7이기때문에 python이 아니라 python3 명령어를 사용하는것이 좋다
.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	virtualenv venv; \
	. .venv/bin/activate; \
	pip install -r requirements.txt;

tests:
	. .venv/bin/activate; \
	python3 manage.py test

run:
	. .venv/bin/activate; \
	python3 manage.py run

all: clean install tests run
