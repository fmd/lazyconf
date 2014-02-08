from setuptools import setup

l = 'lazyconf/'
s = l + 'schema/'
t = s + 'test/'

setup(
    name='lazyconf',
    version='0.3.5',
    author='Fareed Dudhia',
    author_email='fareeddudhia@gmail.com',
    package_dir={'' : 'lazyconf'},
    packages=['lib'],
    entry_points={
        'console_scripts': ['lazyconf = console:conf',]},
    data_files=[(t, [t + 'invalid.json',t + 'valid.json', t + 'noobject.json']),
                (s, [s +'django.json', s + 'empty.json'])],
    url='https://www.github.com/fmd/lazyconf',
    license='LICENSE.rst',
    description='Insultingly simple configuration for Python 2.7 applications.',
    long_description=open('README.md').read(),
)
