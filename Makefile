vpath %.whl ./dist
vpath %.tar.gz ./dist
vpath %.py ./src/astroid_miner ./tests

build: %.whl %.tar.gz

%.whl %.tar.gz: pyproject.toml clean
	python -m build

pypi: build
	python -m twine upload dist/*

test_pypi: build
	python -m twine upload --repository testpypi dist/*

clean:
	rm -f dist/*
