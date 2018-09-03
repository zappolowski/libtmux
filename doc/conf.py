# -*- coding: utf-8 -*-
import inspect
import os
import sys
from os.path import dirname, relpath

import alagitpull

import libtmux  # NOQA
from libtmux import test  # NOQA

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

sys.path.insert(0, project_root)


# package data
about = {}
with open("../libtmux/__about__.py") as fp:
    exec(fp.read(), about)


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.linkcode',
    'sphinxcontrib.napoleon',
    'releases',
    'alagitpull',
]

releases_unstable_prehistory = True
releases_document_name = "history"
releases_issue_uri = "https://github.com/tmux-python/libtmux/issues/%s"
releases_release_uri = "https://github.com/tmux-python/libtmux/tree/v%s"
releases_future_release_uri = "https://github.com/tmux-python/libtmux/tree/%s"

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = about['__title__']
copyright = about['__copyright__']

version = '%s' % ('.'.join(about['__version__'].split('.'))[:2])
release = '%s' % (about['__version__'])

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme_path = [alagitpull.get_path()]
html_favicon = 'favicon.ico'
html_theme = 'alagitpull'
html_theme_options = {
    'logo': 'img/libtmux.svg',
    'github_user': 'tmux-python',
    'github_repo': 'libtmux',
    'github_type': 'star',
    'github_banner': True,
    'projects': alagitpull.projects,
    'project_name': about['__title__'],
}
alagitpull_internal_hosts = ['libtmux.git-pull.com', '0.0.0.0']
alagitpull_external_hosts_new_window = True

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'more.html',
        'book.html',
        'searchbox.html',
    ]
}

html_theme_path = ['_themes']
html_static_path = ['_static']

htmlhelp_basename = '%sdoc' % about['__title__']

latex_documents = [
    (
        'index',
        '{0}.tex'.format(about['__package_name__']),
        '{0} Documentation'.format(about['__title__']),
        about['__author__'],
        'manual',
    )
]

man_pages = [
    (
        'index',
        about['__package_name__'],
        '{0} Documentation'.format(about['__title__']),
        about['__author__'],
        1,
    )
]

texinfo_documents = [
    (
        'index',
        '{0}'.format(about['__package_name__']),
        '{0} Documentation'.format(about['__title__']),
        about['__author__'],
        about['__package_name__'],
        about['__description__'],
        'Miscellaneous',
    )
]

intersphinx_mapping = {'http://docs.python.org/': None}


def linkcode_resolve(domain, info):  # NOQA: C901
    """
    Determine the URL corresponding to Python object

    Notes
    -----
    From https://github.com/numpy/numpy/blob/v1.15.1/doc/source/conf.py, 7c49cfa
    on Jul 31. License BSD-3. https://github.com/numpy/numpy/blob/v1.15.1/LICENSE.txt
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    fn = relpath(fn, start=dirname(libtmux.__file__))

    if 'dev' in about['__version__']:
        return "%s/blob/master/%s/%s%s" % (
            about['__github__'],
            about['__package_name__'],
            fn,
            linespec,
        )
    else:
        return "%s/blob/v%s/%s/%s%s" % (
            about['__github__'],
            about['__version__'],
            about['__package_name__'],
            fn,
            linespec,
        )
