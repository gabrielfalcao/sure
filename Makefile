MAKEFILE_PATH		:= $(realpath $(firstword $(MAKEFILE_LIST)))
GIT_ROOT		:= $(shell dirname $(MAKEFILE_PATH))
VENV_ROOT		:= $(GIT_ROOT)/.venv

PACKAGE_NAME		:= sure
MAIN_CLI_NAME		:= sure
REQUIREMENTS_FILE	:= development.txt

PACKAGE_PATH		:= $(GIT_ROOT)/$(PACKAGE_NAME)
REQUIREMENTS_PATH	:= $(GIT_ROOT)/$(REQUIREMENTS_FILE)
MAIN_CLI_PATH		:= $(VENV_ROOT)/bin/$(MAIN_CLI_NAME)
export VENV		?= $(VENV_ROOT)

OSNAME			:= $(shell uname)
ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif
export SURE_NO_COLORS := true

######################################################################
# Phony targets (only exist for typing convenience and don't represent
#                real paths as Makefile expects)
######################################################################

# default target when running `make` without arguments
all: | $(MAIN_CLI_PATH)

# creates virtualenv
venv: | $(VENV)

# updates pip and setuptools to their latest version
develop: | $(VENV)/bin/python $(VENV)/bin/pip

# installs the requirements and the package dependencies
setup: | $(MAIN_CLI_PATH)

# Convenience target to ensure that the venv exists and all
# requirements are installed
dependencies:
	@rm -f $(MAIN_CLI_PATH) # remove MAIN_CLI_PATH to trigger pip install
	$(MAKE) develop setup

docs:
	@(cd docs && make html)
	$(OPEN_COMMAND) docs/build/html/index.html

test tests: clean | $(VENV)/bin/pytest # $(VENV)/bin/nosetests	# @$(VENV)/bin/nosetests --rednose --immediate -vv --with-coverage --cover-package=sure
	@$(VENV)/bin/pytest -vv --cov=sure tests/unit tests/functional

# run main command-line tool
run: | $(MAIN_CLI_PATH)
	$(MAIN_CLI_PATH) --immediate tests/runner/test_eins.py
	$(MAIN_CLI_PATH) --immediate tests/runner/

# Pushes release of this package to pypi
push-release: dist  # pushes distribution tarballs of the current version
	$(VENV)/bin/twine upload dist/*.tar.gz

# Prepares release of this package prior to pushing to pypi
build-release:
	$(VENV)/bin/python setup.py build sdist
	$(VENV)/bin/twine check dist/*.tar.gz

# Convenience target that runs all tests then builds and pushes a release to pypi
release: tests
	@./.release
	$(MAKE) build-release
	$(MAKE) push-release

# Convenience target to delete the virtualenv
clean:
	@rm -rf .coverage

# Convenience target to format code with black with PEP8's default
# 80 character limit per line
black: | $(VENV)/bin/black
	@$(VENV)/bin/black -l 80 $(PACKAGE_PATH) tests

##############################################################
# Real targets (only run target if its file has been "made" by
#               Makefile yet)
##############################################################

# creates virtual env if necessary and installs pip and setuptools
$(VENV): | $(REQUIREMENTS_PATH)  # creates $(VENV) folder if does not exist
	echo "Creating virtualenv in $(VENV_ROOT)" && python3 -mvenv $(VENV)

# installs pip and setuptools in their latest version, creates virtualenv if necessary
$(VENV)/bin/python $(VENV)/bin/pip: # installs latest pip
	@test -e $(VENV)/bin/python || $(MAKE) $(VENV)
	@test -e $(VENV)/bin/pip || $(MAKE) $(VENV)
	@echo "Installing latest version of pip and setuptools"
	@$(VENV)/bin/pip install -U pip setuptools

 # installs latest version of the "black" code formatting tool
$(VENV)/bin/black: | $(VENV)/bin/pip
	$(VENV)/bin/pip install -U black

# installs this package in "edit" mode after ensuring its requirements are installed

$(VENV)/bin/nosetests $(VENV)/bin/pytest $(MAIN_CLI_PATH): | $(VENV) $(VENV)/bin/pip $(VENV)/bin/python $(REQUIREMENTS_PATH)
	$(VENV)/bin/pip install -r $(REQUIREMENTS_PATH)
	$(VENV)/bin/pip install -e .

# ensure that REQUIREMENTS_PATH exists
$(REQUIREMENTS_PATH):
	@echo "The requirements file $(REQUIREMENTS_PATH) does not exist"
	@echo ""
	@echo "To fix this issue:"
	@echo "  edit the variable REQUIREMENTS_NAME inside of the file:"
	@echo "  $(MAKEFILE_PATH)."
	@echo ""
	@exit 1

###############################################################
# Declare all target names that exist for convenience and don't
# represent real paths, which is what Make expects by default:
###############################################################

.PHONY: \
	all \
	black \
	build-release \
	clean \
	dependencies \
	develop \
	push-release \
	release \
	setup \
	run \
	test \
	tests \
	docs
