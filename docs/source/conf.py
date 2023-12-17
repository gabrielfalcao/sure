import sys
import os
import sphinx_rtd_theme
os.environ['SURE_DISABLE_NEW_SYNTAX'] = 'true'

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
copyright = "2015-2023, Gabriel Falcão"
author = "Gabriel Falcão"
version = "3.0.0a"
release = "3.0.0a"
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
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
}
