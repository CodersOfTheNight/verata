# Verata
Yet another scraper
[![Build Status](https://travis-ci.org/CodersOfTheNight/verata.svg?branch=master)](https://travis-ci.org/CodersOfTheNight/verata)
[![Coverage Status](https://coveralls.io/repos/github/CodersOfTheNight/verata/badge.svg?branch=master)](https://coveralls.io/github/CodersOfTheNight/verata?branch=master)
[![Documentation Status](https://readthedocs.org/projects/verata/badge/?version=latest)](http://verata.readthedocs.io/en/latest/?badge=latest)

Why even consider?
------------------
It works just by providing correct config - no coding is required

How to install
--------------
`pip install verata` 

Supported versions
------------------
It is tested on Python versions:
- 2.7
- 3.4
- 3.5

Usage
-----
**As crawler**(Travel trough whole page):

`verata --config=config-file.yml --output=<output_file> crawl`

Optionally you can setup environment file:

`verata --config=config-file.yml --env=.secret-env --output=<output_file> crawl`

**As scraper**(Only read concrete link):

`verata --config=config-file.yml --output=<output_file> scrape --link=<actual url>`

Docs
----
[http://verata.readthedocs.io](http://verata.readthedocs.io/en/latest/)

CLI Params
----------
- `--env` - environment file (default: .env). It is used to cointain variables which you don't want to expose in config (eg. password, username)
- `--config` - congiration file (default: config.yml)
- `--log_level` - select logging level (default: INFO)
- `--debug` - shortcut for logging level DEBUG
- `--output` - file in which results are being kept
- `--paginate` - (Only makes sense if `rest_interval` is more than 0 seconds) crawl pages in chunks, resting after each chunk. Used to avoid being banned/bring site down.
- `--rest_interval` - time to rest between chunks (default: `10s`). Letter at the end tells in which format: `s` - seconds, `m` - minutes, `h` - hours.

Config example
--------------
```yaml
---
name: Python Org scrapper
description: Just scrape it for testing
site_root: https://www.python.org
start_page: /blogs
cookies:
  authToken: abc1234
  remember: true
headers:
  "User-Agent": "Mozilla/5"
pages:
  - name: Blog
    link_pattern: /blog%
    mappings:
      - name: title
        path: h3[class="event-title"]/a
```


It support login to website as well...
--------------------------------------
```yaml
name: A super secret page
description: Only we have access
site_root: http://page.secret
start_page: /restricted_area
auth:
  url: /login
  method: POST
  params:
    user: {{ secret_user }}
    password: {{ secret_password }}
```

Locked web is a big part of the internet, however it is rarely accessed by scrappers.
This tool gives you possibility to login to some of them (CAPTCHA is a bit pain).

Variables `secret_user` and `secret_password` are being picket from file `.env`
which would look like this:
```bash
secret_user=demo
secret_password=demo
```

It is done like this, because usually there are some variables we don't want to expose in config and put to any source control system.

Version history
---------------
1.2:
  - introduced scraping functionallity
  - fixed some bugs in data collection process
  
1.1:
  - args parsed from same page are grouped into array
  
  - selected elements by `path` now provides all atributes together with element text
  
1.0 - basic functionallity
