 
Configuration
=============

Config
------

============    =================       ======================================
Value           Notes                   Description
============    =================       ======================================
name                                    A user-friendly name for config
description                             Description about config
site_root                               Site url which we will be scrapping
start_page                              Where to start our scrapping
cookies         (Optional, Array)       Add cookies to our requests
headers         (Optional, Array)       Add headers to our requests
proxies         (Optional, Array)       Add http proxies to our requests
pages           (Array)                 Consists an array of `Page`
parser          (Optional)              Select parser for web pages.
auth            (Optional)              `Auth` object
============    =================       ======================================


Auth
----

============    ================       ======================================
Value           Notes                   Description
============    ================       ======================================
url                                     Login url
method          (Optional)              Default: POST, you can add any other http method
params          (Array)                 Key-Value pairs for request
============    ================       ======================================

Page
----

============    ================       ======================================
Value           Notes                   Description
============    ================       ======================================
name                                    Name of page
link_pattern                            Pattern which allows to detect which page parser to use
mappings        (Array)                 Array of `Mapping`
============    ================       ======================================

Mapping
-------

============    ================       ======================================
Value           Notes                   Description
============    ================       ======================================
name                                    Name of mapping
path                                    Path to element
============    ================       ======================================
