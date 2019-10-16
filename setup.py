from setuptools import setup, find_packages

from password_generator import __version__


setup(
    name='passgen',
    version=__version__,
    url='https://github.com/k4m454k/PyPasswordGenerator/tree/master/password_generator',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().split(),
    entry_points={
        'console_scripts': [
            'passgen = password_generator.passgen:entrypoint',
        ],
    },
)
