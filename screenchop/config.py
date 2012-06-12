#!/usr/bin/env python

from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

# Read config.ini and store into variables
HOST = config.get('app', 'HOST')
PORT = int(config.get('app', 'PORT'))
DEBUG = config.get('app', 'DEBUG')
TEMP_FILE_DIR = config.get('app', 'TEMP_FILE_DIR')

# Mongo Configs
MONGO_DATABASE = config.get('mongodb', 'DATABASE')
MONGO_HOST = config.get('mongodb', 'HOST')
MONGO_PORT = int(config.get('mongodb', 'PORT'))
MONGO_USER = config.get('mongodb', 'USER')
MONGO_PASS = config.get('mongodb', 'PASS')

# S3 Configs
BUCKET_NAME = config.get('s3', 'BUCKET_NAME')
AWS_ACCESS_KEY_ID = config.get('s3', 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('s3', 'AWS_SECRET_ACCESS_KEY')
S3_THUMBS_URL = config.get('s3', 'S3_THUMBS_URL')
