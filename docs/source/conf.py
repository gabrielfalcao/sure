# -*- coding: utf-8 -*-
# <sure - sophisticated automated test library and runner>
# Copyright (C) <2010-2024>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
version = "3.0a0"
release = "3.0a0"
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
        "sophisticated automated test library and runner for python.",
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
