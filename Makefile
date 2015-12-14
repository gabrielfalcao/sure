# Config
OSNAME			:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif

all: install_deps test

filename=sure-`python -c 'import sure;print sure.version'`.tar.gz

export PYTHONPATH := ${PWD}:${PYTHONPATH}
export SURE_NO_COLORS := true

install_deps:
	@pip install -r development.txt

test:
	@python setup.py build
	@nosetests -s --verbosity=2 tests --rednose
	@steadymark OLD_API.md
	@steadymark README.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: clean test publish
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) sure setup.py README.md COPYING
	@echo "DONE!"

publish:
	@./.release
	@python setup.py sdist register upload

acceptance: clean
	@steadymark README.md
	@steadymark spec/reference.md


docs: acceptance
	@(cd docs && make html)
	$(OPEN_COMMAND) docs/build/html/index.html
