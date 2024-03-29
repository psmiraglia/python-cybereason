default: install

style: flake8 isort-diff

flake8:
	flake8 setup.py bin/* pycybereason/*.py pycybereason/**/*.py

isort-diff:
	isort --diff setup.py bin/* pycybereason/*.py pycybereason/**/*.py

isort:
	isort setup.py bin/* pycybereason/*.py pycybereason/**/*.py

install:
	pip install .

venv37:
	virtualenv -p python3.7 .venv
