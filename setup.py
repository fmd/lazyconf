from distutils.core import setup

setup(
    name='django-lazyconf',
    version='0.1.0',
    author='Fareed Dudhia',
    author_email='fareeddudhia@gmail.com',
    packages=['lazyconf'],
    scripts=[],
    url='https://www.github.com/fmd/django-lazyconf',
    license='LICENSE.txt',
    description='Lazy config and deployment for Django.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.7",
        "Fabric >= 1.8.1"
    ],
)