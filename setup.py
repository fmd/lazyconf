from setuptools import setup

setup(
    name='lazyconf',
    version='0.1',
    author='Fareed Dudhia',
    author_email='fareeddudhia@gmail.com',
    packages=['lazyconf'],
    scripts=[],
    url='https://www.github.com/fmd/lazyconf',
    license='LICENSE.rst',
    description='Lazy config and deployment for Django.',
    long_description=open('README.rst').read(),
    install_requires=[
        "Fabric >= 1.8"
    ],
)
