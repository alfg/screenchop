#!/usr/bin/env python

from setuptools import setup

setup(name='screenchop',
      version='0.1',
      description='A Screenshot Sharing WebApp for Gamers',
      author='Alf',
      author_email='alf.g.jr@gmail.com',
      packages=['screenchop'],
      install_requires=['Flask', 'mongoengine', 'boto', 'flask-bcrypt', 'flask-wtf']
)

