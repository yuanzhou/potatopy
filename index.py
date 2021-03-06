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

import os

# Set the 'PYTHON_EGG_CACHE' cache environment variable
# to a directory which is owned and/or writable by the user that Apache runs as
# This fixes the Python egg cache directory error
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-eggs'
import sys

from potatopy.core.wsgi_starter import WSGI_Starter

# This is our application object - WSGI application entry point 
# mod_wsgi requires that the WSGI application entry point be called 'application'.
# If you want to call it something else then you would need to configure mod_wsgi explicitly to use the other name
# The WSGI application will be run as the user that Apache runs as
application = WSGI_Starter()


