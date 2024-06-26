import os
import sys

# Configuration file for the Sphinx documentation builder.
#

# -- Project information -----------------------------------------------------

project = "sentry-kafka-schemas"
copyright = "2023, Sentry Team and Contributors"
author = "Sentry Team and Contributors"

sys.path.insert(0, os.path.abspath("../../python/"))
sys.path.insert(0, os.path.abspath("."))

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mermaid",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
]

always_document_param_types = True

# This is relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["build"]

pygments_style = "sphinx"

source_suffix = ".rst"

# -- Options for HTML output -------------------------------------------------

html_theme = "shibuya"

html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

# html_logo = "_static/arroyo.png"

autodoc_inherit_docstrings = False

mermaid_init_js = "mermaid.initialize({startOnLoad:true, flowchart:{defaultRenderer: 'elk'}});"
