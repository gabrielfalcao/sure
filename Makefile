# Config
OSNAME			:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif
VENV			?= .venv
all: install_deps test

filename=sure-`python -c 'import sure;print(sure.version)'`.tar.gz

export PYTHONPATH := ${PWD}:${PYTHONPATH}
export SURE_NO_COLORS := true

$(VENV):
	python3 -mvenv $(VENV)

$(VENV)/bin/pip: | $(VENV)
	$(VENV)/bin/pip install -U setuptools pip

$(VENV)/bin/twine $(VENV)/bin/pytest $(VENV)/bin/nosetests: | $(VENV)/bin/pip
	$(VENV)/bin/pip install -r development.txt


sure.egg-info/PKG-INFO: | $(VENV)/bin/nosetests  $(VENV)/bin/pytest
	@$(VENV)/bin/python setup.py develop

test: sure.egg-info/PKG-INFO
	@$(VENV)/bin/pytest
	@$(VENV)/bin/nosetests --rednose --immediate -vv --with-coverage --cover-package=sure

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

publish:
	@$(VENV)/bin/python setup.py sdist
	@$(VENV)/bin/twine upload dist/*.tar.gz

release: clean test publish

.PHONY: docs

docs:
	@(cd docs && make html)
	$(OPEN_COMMAND) docs/build/html/index.html
