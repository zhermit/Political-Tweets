try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Prospectus 0.1. Analyzes media sources for agenda setting capacity',
    'author': 'Galen Stocking',
    'url': 'none.',
    'download_url': 'none.',
    'author_email': 'none.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['PROSPECTUS'],
    'scripts': [],
    'name': 'prospectus'
}

setup(**config)