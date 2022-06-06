default: install

flake8:
	flake8 setup.py bin/* pycybereason/*.py

isort-diff:
	isort --diff setup.py bin/* pycybereason/*.py

isort:
	isort setup.py bin/* pycybereason/*.py

install:
	pip install .
