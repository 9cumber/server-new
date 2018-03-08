SHELL := /bin/sh

deps: 
	pipenv install --dev --two

clean:
	find . -name '*.pyc' | xargs rm -rf

yapf:
	pipenv run yapf -ri cucumber test

export-lib:
	pipenv lock --requirements > requirements.txt
	pipenv run pip install -r requirements.txt -t lib

run:
	pipenv run python -m cucumber.endpoint

test: clean test-pytest test-pylint test-yapf

test-pytest:
	pipenv run pytest

test-pylint:
	pipenv run pylint cucumber

test-yapf:
	test $(shell pipenv run yapf --diff -r cucumber | wc -l) -eq 0

.PHONY: deps clean yapf test test-pytest test-pylint test-yapf export-lib
