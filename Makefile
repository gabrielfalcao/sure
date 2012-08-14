all: install_deps test

filename=sure-`python -c 'import sure;print sure.version'`.tar.gz

export PYTHONPATH:=  ${PWD}

install_deps:
	@pip install -r requirements.pip

test:
	@steadymark README.md
	@nosetests --verbosity=2 test_sure.py
	@steadymark OLD_API.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: clean test publish
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) sure setup.py README.md COPYING
	@echo "DONE!"

publish:
	@python setup.py sdist register upload
