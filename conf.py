# Configuration file for the Sphinx documentation builder.
#
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx
import sys
import os

# -- Project information

project = "Returned"
copyright = "Returned. A non-commercial mod fork. Not affiliated with Smartly Dressed Games."
author = "SomeAussieGamer"

version = "0.0.1"
release = version

# -- General configuration
sys.path.append(os.path.abspath("_extensions")) # also find extensions within this directory
extensions = [
    "notfound.extension",  # Adds custom "404 Not Found" page
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_copybutton',
    'sphinx.ext.intersphinx',
    'sphinxext.opengraph', # OpenGraph support (e.g., URLs posted offsite appear as OneBox embeds)
    'sphinx_tabs.tabs',
    # -- Locally-installed modules
    'unturned_lexer',
]

exclude_patterns = [
    '.venv/*' # Contains installed packages which may have .rst files we don't want included in source files.
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

# https://sphinx-themes.org/sample-sites/groundwork-sphinx-theme/
html_theme = "groundwork"

# Groundwork's FlaskyStyle is a light theme (black tokens + underlined
# whitespace). Override so code stays readable on Groundwork's dark panels.
pygments_style = "monokai"

html_theme_options = {
    "sidebar_width": "300px",
    "stickysidebar": True,
    "stickysidebarscrollable": True,
}

# Groundwork/basic defaults to localtoc ("This page" headings) + next/prev.
# Use the full site tree so every section is listed without clicking Next.
html_sidebars = {
    "**": [
        "globaltoc.html",
        "searchbox.html",
    ]
}

# Define the canonical URL if you are using a custom domain on Read the Docs
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# These folders are copied to the documentation's HTML output
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (e.g. https://...)
html_css_files = [
    'css/custom.css',
    'css/toctree_collapse.css',
]

html_js_files = [
    'js/toctree_collapse.js',
]

# -- Options for EPUB output
epub_show_urls = 'footnote'
