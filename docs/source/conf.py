import sys
import os
import sphinx_rtd_theme
from pathlib import Path
try:
    import sure
    import sure.original
    import sure.core
    import sure.runtime
    import sure.runner
    import sure.doubles
    import sure.meta
    import sure.reporter
    import sure.reporters.feature
except ImportError:
    sys.path.insert(0, Path(__file__).parent.parent.parent)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
]

source_suffix = ".rst"
master_doc = "index"
project = "sure"
copyright = "2010-2024, Gabriel Falcão"
author = "Gabriel Falcão"
version = "3.0dev0"
release = "3.0dev0"
language = 'en'
exclude_patterns = []
pygments_style = "sphinx"
todo_include_todos = True

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# html_static_path = ["_static"]
htmlhelp_basename = "sure_"
latex_elements = {}
latex_documents = [
    (master_doc, "Sure.tex", "Sure Documentation", "Gabriel Falcão", "manual"),
]
man_pages = [(master_doc, "sure", "Sure Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        "Sure",
        "Sure Documentation",
        author,
        "Sure",
        "utility belt for automated testing in python for python.",
        "Automated Testing",
    ),
]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ["search.html"]
intersphinx_disabled_reftypes = []
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "mock": ("https://mock.readthedocs.io/en/latest/", None),
    "psycopg2": ("https://www.psycopg.org/docs/", None),
    "coverage": ("https://coverage.readthedocs.io/en/7.3.3/", None),
}
pygments_style = 'xcode'
