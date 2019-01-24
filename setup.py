"""setup.py file."""

#import uuid

from setuptools import setup, find_packages
#from pip.req import parse_requirements


with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

__author__ = 'Michel Barbosa <github.com/barbosm>'

setup(
    name="napalm-fortios6",
    version="0.1.0",
    packages=find_packages(),
    author="Michel Barbosa",
    author_email="barbosm@noreply.github.com",
    description="Network Automation and Programmability Abstraction Layer with Multivendor support",
    classifiers=[
        'Topic :: Utilities',
         'Programming Language :: Python',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/barbosm/napalm-fortios6",
    include_package_data=True,
    install_requires=reqs,
)
