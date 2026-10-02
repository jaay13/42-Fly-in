.PHONY: install run debug clean lint lint-strict test

MAP ?= maps/easy/01_linear_path.txt

MYPY_FLAGS = --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

install:
	pip install -r requirements-dev.txt

run:
	python3 fly_in.py $(MAP)

debug:
	python3 -m pdb fly_in.py $(MAP)

clean:
	find . \( -path './.venv*' -o -path './venv*' \) -prune -o \
		\( -name '__pycache__' -o -name '.pytest_cache' \
		   -o -name '*.py[co]' \) \
		-exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

test:
	python3 -m pytest tests
