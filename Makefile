# Config
OSNAME			:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif

all: install_deps test

filename=sure-`python -c 'import sure;print(sure.version)'`.tar.gz

export PYTHONPATH := ${PWD}:${PYTHONPATH}
export SURE_NO_COLORS := true

install_deps:
	@pipenv install --dev

test:
	@pipenv run python setup.py develop
	@pipenv run nosetests --rednose --immediate -vv --with-coverage --cover-package=sure


clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"


publish:
	@python setup.py sdist
	@twine upload dist/*.tar.gz

release: clean test publish

.PHONY: docs

docs:
	@(cd docs && make html)
	$(OPEN_COMMAND) docs/build/html/index.html
