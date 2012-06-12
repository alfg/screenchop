#!/usr/bin/env python

from screenchop import urls
from screenchop import config

app = urls.app

# Return an App
if __name__ == "__main__":
    urls.app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
