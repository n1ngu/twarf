
import codecs
import re
from setuptools import setup, find_packages
import os.path


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = '([^']*)'",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = read('README.md')
version = find_version('twarf', 'version.py')

setup(
    name='twarf',
    version=version,
    description='Twisted Web Application Firewall',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nobody',
    author_email='nobody@mierdamail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'twisted',
        'cryptography',
    ],
    tests_require=[
        'aiounittest',
    ],
    extras_require={
        'dev': [
            'check-manifest',
            'aiounittest',
        ],
    },
    entry_points={
        'console_scripts': [
            'twarf=twarf.__main__:main',
        ],
    },
)
