##############################################################################
#
# Copyright (c) 2013-2014 Zhou Yuan <yuanzhou19@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT license at
# http://www.opensource.org/licenses/mit-license.php
#
##############################################################################

""" 
PotatoPy
--------

PotatoPy is a very lightweight, well-designed, well-documented, and fully WSGI compatible Python Web Development Framework loosely built around HTTP in a RESTful approach. It incorporated many good ideas and useful components from other well-known web frameworks and toolkits. Working with PotatoPy in a structured and rapid manner enables web developers to create efficient, extensible, and maintainable web applications.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='PotatoPy',
    version='0.10-dev',
    url='http://potatopy.com/',
    license='MIT',
    author='Zhou (Joe) Yuan',
    author_email='yuanzhou19@gmail.com',
    description='The lighter, faster Python Framework',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['potatopy', 'potatopy.core'],
    include_package_data=True,
    zip_safe=False,
    platforms='any'
)