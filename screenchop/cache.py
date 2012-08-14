""" Caching configuration. Use from screenchop.cache import cache """

from flask import Flask
from flaskext.cache import Cache
from screenchop import config

app = Flask(__name__)
app.config['CACHE_TYPE'] = config.CACHE_TYPE
app.config['CACHE_MEMCACHED_SERVERS'] = config.CACHE_SERVER_ADDRESS
cache = Cache(app)
