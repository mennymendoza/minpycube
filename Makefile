init:
	pip install -r requirements.txt

build:
	python3 -m build

test:
	python3 -m pytest
