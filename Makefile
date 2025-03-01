MAKEFILE_PATH		:= $(realpath $(firstword $(MAKEFILE_LIST)))
GIT_ROOT		:= $(shell dirname $(MAKEFILE_PATH))
VENV_ROOT		:= $(GIT_ROOT)/.venv

PACKAGE_NAME		:= sure
LIBEXEC_NAME		:= sure

PACKAGE_PATH		:= $(GIT_ROOT)/$(PACKAGE_NAME)
LIBEXEC_PATH		:= $(VENV_ROOT)/bin/$(LIBEXEC_NAME)
export VENV		?= $(VENV_ROOT)
OSNAME			:= $(shell uname)
ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif
export SURE_NO_COLORS	:= true
export SURE_LOG_FILE	:= $(GIT_ROOT)/sure-$(date +"%Y-%m-%d-%H:%M:%S").log
export PYTHONPATH	:= $(GIT_ROOT)
AUTO_STYLE_TARGETS	:= sure/runtime.py sure/runner.py sure/meta.py sure/meta.py sure/reporter.py sure/reporters


all: tests html-docs autostyle build-release

clean-docs:
	@rm -rf ./docs/build

html-docs: clean-docs
	@cd ./docs && make html

docs: html-docs
	$(OPEN_COMMAND) docs/build/html/index.html

test:
	@uv run pytest --cov=sure tests

tests: clean test run

run:
	uv run sure --reap-warnings tests/crashes
	uv run sure --reap-warnings --special-syntax --with-coverage --cover-branches --cover-erase --cover-module=sure --immediate --cover-module=sure --ignore tests/crashes tests

push-release: dist
	uv build
	uv run twine upload dist/*.tar.gz

build-release:
	uv build
	uv run twine check dist/*.tar.gz

release: tests
	@./.release
	$(MAKE) build-release
	$(MAKE) push-release

clean:
	@rm -rf .coverage

flake8:
	@uv run flake8 --statistics --max-complexity 17 --exclude=$(VENV) $(AUTO_STYLE_TARGETS)

black:
	@uv run black -l 80 $(AUTO_STYLE_TARGETS)

isort:
	@uv run isort --overwrite-in-place --profile=black --ls --srx --cs --ca -n --ot --tc --color --star-first --virtual-env $(VENV) --py auto $(AUTO_STYLE_TARGETS)


autostyle: isort black flake8


.PHONY: \
	all \
	autostyle \
	black \
	build-release \
	clean \
	clean-docs \
	dependencies \
	develop \
	docs \
	flake8 \
	html-docs \
	isort \
	push-release \
	release \
	run \
	test \
	tests
