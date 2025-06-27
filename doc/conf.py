# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Slide Text Bridge'
copyright = '2025, Norihiro Kamae'
author = 'Norihiro Kamae'
language = 'en'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
locale_dirs = ['_locale/']

root_doc = 'index'

html_copy_source = False
html_show_copyright = False
html_theme_options = {
        'extra_nav_links': {
            'Gallery': 'https://github.com/norihiro/slidetextbridge/wiki/Gallery',
            'Source Code': 'https://github.com/norihiro/slidetextbridge/',
        },
}

gettext_compact = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
