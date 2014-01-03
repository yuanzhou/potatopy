##############################################################################
#
# Copyright (c) 2013-2014 Zhou Yuan <yuanzhou19@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT license at
# http://www.opensource.org/licenses/mit-license.php
#
##############################################################################

# WSGI application script 
# Deploying PotatoPy with Apache with mod_wsgi is the recommended way into production

import sys

from wsgiref.simple_server import make_server

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
	# Add module directory to Python's search path
    sys.path.insert(1, path)

from potatopy.core.wsgi_starter import WSGI_Starter

# This is our application object - WSGI application entry point 
# mod_wsgi requires that the WSGI application entry point be called 'application'.
# If you want to call it something else then you would need to configure mod_wsgi explicitly to use the other name
# The WSGI application will be run as the user that Apache runs as
application = WSGI_Starter()

# The first parameter '0.0.0.0' means "listen on all TCP interfaces."
httpd = make_server('0.0.0.0', 8000, application)
print("Listening on port 8000....")
# It runs until explicitly interrupted, either with Ctrl-C or 
# via a suitable signal (a simple kill on Unix will do it).
httpd.serve_forever()


