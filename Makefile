all: install_deps test

filename=sure-`python -c 'import sure;print sure.version'`.tar.gz

export PYTHONPATH := ${PWD}:${PYTHONPATH}
export SURE_NO_COLORS := true

install_deps:
	@curd install -r requirements.txt

test:
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
	@python setup.py sdist register upload

docstests: clean
	@steadymark README.md
	@steadymark spec/*.md

docs: docstests
	@markment --server -o . -t modernist --sitemap-for="http://falcao.it/sure" spec
	@git co master && \
		(git br -D gh-pages || printf "") && \
		git checkout --orphan gh-pages && \
		markment -o . -t modernist --sitemap-for="http://falcao.it/sure" spec && \
		git add . && \
		git commit -am 'documentation' && \
		git push --force origin gh-pages && \
		git checkout master
