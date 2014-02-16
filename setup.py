import sys
from setuptools import setup, find_packages
import lazyconf

l = 'lazyconf/'
s = 'schema/'

setup(
    name='lazyconf',
    version='0.5.1',
    author='Fareed Dudhia',
    author_email='fareeddudhia@gmail.com',
    packages=find_packages(),
    package_data={"lazyconf": ['schema/' 'lazyconf/schema/*.json',]},
    include_package_data=True,
    py_modules=['lazyconf.lazyconf','lazyconf.console'],
    entry_points={
        'console_scripts': ['lazyconf = lazyconf.console:console',]},
    url='https://www.github.com/fmd/lazyconf',
    license='LICENSE.rst',
    description='Insultingly simple configuration for Python 2.7 applications.',
    long_description=open('README.rst').read(),
)
