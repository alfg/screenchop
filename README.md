Screenchop
=======

A screenshot sharing web-application for gamers.

http://screenchop.com

### Technology Stack
- Python (Flask Framework)
- MongoDB with Mongoengine ORM
- Memcached for caching
- AWS S3 for image storage using BOTO library

### Install

Assuming you have a Python environment and MongoDB installed:

Install packages

`pip install -r requirements.txt`

Configure `config.ini.sample` and rename to `config.ini`

Run development server

`python runserver.py` will create MongoDB collections and start development server

`wsgi.py` is provided for using a production server, such as gunicorn.

### manage.py

`python manage.py invite_code` generates an invite code if running screenchop in 
invitation mode.

`python manage.py tag_freq` will populate/update a table with updated tags for performance reasons

You can use the `scripts` folder for ideas on how to use a cron job to update tags on an interval

### License

The MIT License (MIT)

Copyright (c) 2012-2014 Alfred Gutierrez alfg.co

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
