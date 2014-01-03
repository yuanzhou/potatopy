##############################################################################
#
# Copyright (c) 2013-2014 Zhou Yuan <yuanzhou19@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT license at
# http://www.opensource.org/licenses/mit-license.php
#
##############################################################################

import os

import sys

from string import Template

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
    # Add module directory to Python's search path
    sys.path.insert(1, path)

from application.configs.constants import APP_LOG_DIR, SYS_CORE_DIR
from potatopy.core.logger import Logger

class Common(object):
    """ Common shared functions """
    
    @staticmethod
    def handle_error(msg):
        # Log to caputre all errors since some errors can't be manually captured
        Logger.log(APP_LOG_DIR, 'ERROR', __name__, msg)

    
        # No need to explicitly call f.close() since with ... as
        with open(SYS_CORE_DIR + 'sys_templates/sys_error.html', 'r') as f:
            template_content = f.read()
        
        template_vars = {'msg': msg}

        # These are HTTP headers expected by the client.
        # They must be wrapped as a list of tupled pairs:
        # [(Header name, Header value)].
        response_headers = [('Content-Type', 'text/html; charset=utf-8')]
        
        response_content = Template(template_content).substitute(template_vars)

        # Return the response body.
        # Notice it is wrapped in a list although it could be any iterable.
        return {'headers': response_headers, 'content': response_content}

    