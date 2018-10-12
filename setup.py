import os
from setuptools import setup

from wagtailstreamfieldforms import __version__

install_requires = [
    'Django>=1.11,<1.12',
    'wagtail>2,<3',
]

documentation_extras = [
    'Sphinx>=1.7.1',
]

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
#os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="wagtailstreamfieldforms",
    version=__version__,
    packages=['wagtailstreamfieldforms'],
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'docs': documentation_extras,
    },
    license="MIT",
    description="Streamfield Forms allows you to create a form by including the form fields in the content stream of a Wagtail Page.",
    long_description=README,
    url="https://www.github.com/didorothy/wagtailstreamfieldforms", # TODO: commit to this repo or update
    author="David Dorothy",
    author_email="ddorothy@positiveaction.org",
    keywords=['wagtail', 'streamfield', 'forms'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)