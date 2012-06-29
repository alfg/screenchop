#!/usr/bin/env python

from screenchop import urls
from screenchop import config

# app = GUnicorn Hook
app = urls.app
app.config['DEBUG'] = config.DEBUG
