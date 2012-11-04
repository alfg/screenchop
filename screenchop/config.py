#!/usr/bin/env python

from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

# Read config.ini and store into variables
HOST = config.get('app', 'HOST')
PORT = int(config.get('app', 'PORT'))
DEBUG = config.getboolean('app', 'DEBUG')
TEMP_FILE_DIR = config.get('app', 'TEMP_FILE_DIR')
SESSION_KEY = config.get('app', 'SESSION_KEY')
DOMAIN_URL = config.get('app', 'DOMAIN_URL')
SHORT_DOMAIN_URL = config.get('app', 'SHORT_DOMAIN_URL')

# Caching Configs
CACHE_TYPE = config.get('caching', 'CACHE_TYPE')
CACHE_SERVER_ADDRESS = config.get('caching', 'CACHE_SERVER_ADDRESS').split()
CACHE_DEFAULT_TIMEOUT = config.getint('caching', 'CACHE_DEFAULT_TIMEOUT')

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
S3_MEDIUM_URL = config.get('s3', 'S3_MEDIUM_URL')
S3_FULL_URL = config.get('s3', 'S3_FULL_URL')
S3_AVATAR_URL = config.get('s3', 'S3_AVATAR_URL')

# Registration
REGISTRATION_LEVEL = config.get('registration', 'REGISTRATION_LEVEL')

# Gallery Configs
MAX_IMAGES_PER_ROW = int(config.get('gallery', 'MAX_IMAGES_PER_ROW'))
HOME_MAX_IMAGES = int(config.get('gallery', 'HOME_MAX_IMAGES'))
TAGGING_ENABLED = config.getboolean('gallery', 'TAGGING_ENABLED')

# Upload Configs
ALLOWED_FILE_TYPES = config.get('upload', 'ALLOWED_FILE_TYPES').split(',')
THUMB_MAX_WIDTH = int(config.get('upload', 'THUMB_MAX_WIDTH'))
THUMB_MAX_HEIGHT = int(config.get('upload', 'THUMB_MAX_HEIGHT'))
MEDIUM_MAX_WIDTH = int(config.get('upload', 'MEDIUM_MAX_WIDTH'))
MEDIUM_MAX_HEIGHT = int(config.get('upload', 'MEDIUM_MAX_HEIGHT'))

# Marketing Configs
GOOGLE_ANALYTICS_ACCOUNT = config.get('marketing', 'GOOGLE_ANALYTICS_ACCOUNT')
