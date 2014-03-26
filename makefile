.PHONY: build clean install test test-full release travisci-install travisci-test

##
# Variables
##

ENV_NAME = env
ENV_ACT = . env/bin/activate;
PIP = $(ENV_NAME)/bin/pip
PYTEST_ARGS = --doctest-modules -v -s
PYTEST_TARGET = ladder tests
COVERAGE_ARGS = --cov-config setup.cfg --cov-report term-missing --cov
COVERAGE_TARGET = ladder

##
# Targets
##

# project initialization/clean-up
build: clean install

clean: clean-env clean-files

clean-env:
	rm -rf $(ENV_NAME)

clean-files:
	rm -rf .tox
	rm -rf .coverage
	find . -name \*.pyc -type f -delete
	find . -name \*.test.db -type f -delete
	find . -depth -name __pycache__ -type d -exec rm -rf {} \;
	rm -rf dist *.egg* build

install:
	rm -rf $(ENV_NAME)
	virtualenv --no-site-packages $(ENV_NAME)
	$(PIP) install -r requirements.txt


# testing
test:
	$(ENV_ACT) py.test $(PYTEST_ARGS) $(COVERAGE_ARGS) $(COVERAGE_TARGET) $(PYTEST_TARGET)

test-full:
	rm -rf .tox
	$(ENV_ACT) tox


# linting
lint: pylint pep8

pep8:
	$(ENV_ACT) tox -e pep8

pylint:
	$(ENV_ACT) pylint $(COVERAGE_TARGET)


# code release
release:
	$(ENV_ACT) python setup.py sdist bdist_wheel
	$(ENV_ACT) twine upload dist/*
	rm -rf dist *.egg* build

##
# TravisCI
##

travisci-install:
	pip install -r requirements.txt

travisci-test:
	py.test $(PYTEST_ARGS) $(COVERAGE_ARGS) $(COVERAGE_TARGET) $(PYTEST_TARGET)
