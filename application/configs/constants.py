##############################################################################
#
# Copyright (c) 2013-2014 Zhou Yuan <yuanzhou19@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT license at
# http://www.opensource.org/licenses/mit-license.php
#
##############################################################################

SYS_CORE_DIR = '/Library/WebServer/Documents/potatopy/potatopy/core/'

# The log dir must be writable
APP_LOG_DIR = '/Library/WebServer/Documents/potatopy/application/logs/'

# Logging levels: CRITICAL > ERROR > WARNING > INFO > DEBUG
# DEBUG	- Detailed information, typically of interest only when diagnosing problems.
# INFO - Confirmation that things are working as expected.
# WARNING - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.
# ERROR - Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL - A serious error, indicating that the program itself may be unable to continue running.
APP_LOGGING_LEVEL_THRESHOLD = 'DEBUG'

APP_MANAGER_DIR = '/Library/WebServer/Documents/potatopy/application/managers/'

APP_TEMPLATE_DIR = '/Library/WebServer/Documents/potatopy/application/templates/'

# Case-insensitive
APP_DEFAULT_MANAGER = 'home'

# Case-insensitive
APP_DEFAULT_MANAGER_METHOD = 'index'

# All dynamic resources will be handled by wsgi_mod
# In httpd.conf: 
# WSGIScriptAlias / /Library/WebServer/Documents/potatopy/index.py
APP_URI_BASE = 'http://localhost/'

# All static resources will be handled by Apache
# In httpd.conf: 
# Alias /static/ /Library/WebServer/Documents/potatopy/application/static/
STATIC_URI_BASE = 'http://localhost/static/'