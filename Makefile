all: check_dependencies test

filename=sure-`python -c 'import sure;print sure.version'`.tar.gz

export PYTHONPATH:=  ${PWD}

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@python -c "import nose" 2>/dev/null || (echo "You must install nose in order to run nose's tests" && exit 3)

test: clean
	@echo "Running tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive --cover-package=sure

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: test
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) sure setup.py README.md COPYING
	@echo "DONE!"
