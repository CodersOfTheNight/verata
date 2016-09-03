# Verata
Yet another scraper

Why even consider?
------------------
It works just by providing correct config - no coding is required

How to install
--------------
`pip install verata` 

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
