"""
setup.py
"""
from setuptools import setup

setup (
    name='contracts',
    version='0.1.0',
    author='Rodney Gomes',
    author_email='rodneygomes@gmail.com',
    url='',
    install_requires = ["setuptools"],
    test_suite="test",
    keywords = ['contracts'],
    py_modules = ['contracts'],
    license='Apache 2.0 License',
    description='',
    long_description=open('README').read(),
)