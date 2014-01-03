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

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
    # Add module directory to Python's search path
    sys.path.insert(1, path)
    
from application.configs.constants import APP_LOG_DIR
from potatopy.core.common import Common
from potatopy.core.dispatcher import Dispatcher

class WSGI_Starter(object):
    """ Constructing a WSGI application """     
    
    # The environ points to a dictionary containing CGI like environment variables
    # which is filled by the server for each received incoming request from the client
    # The environ contains all the environment variables
    # REQUEST_METHOD, SCRIPT_NAME, PATH_INFO, QUERY_STRING, CONTENT_TYPE,
    # CONTENT_LENGTH, SERVER_NAME, SERVER_PORT, SERVER_PROTOCOL, HTTP_ variables

    # The start_response is a callback function supplied by the server
    # which will be used to send the HTTP status and headers to the server

    # __call__() allows an instance of a class to be called as a function
    def __call__(self, environ, start_response):

        # Introduce the response dictionary (contains 'headers' and 'content')
        # Caliing dict() is slower than just the literal dictionary syntax {}
        response = {}

        # Initial check
        if os.path.isdir(APP_LOG_DIR):
            if not os.access(APP_LOG_DIR, os.W_OK):
                response = Common.handle_error('APP_LOG_DIR must be writable!')
            else:
                # Dispatcher instance
                dispatcher = Dispatcher(environ)
                # The content and headers of output from response
                # You can also dispatch all requests to the same manager
                # E.g., response = dispatcher.run('maintainence', 'index')
                response = dispatcher.run()
        else:
            response = Common.handle_error('APP_LOG_DIR does not exist!')

        # HTTP response status code
        status = '200 OK'

        # Response headers are HTTP headers expected by the client
        # They must be wrapped as a list of tupled pairs:
        # [(Header name, Header value)].
        start_response(status, response['headers'])

        # Return the response body.
        # Notice it is wrapped in a list although it could be any iterable.
        # Python 3.x requires the returned string to be bytes: return [b"Hello World"] 
        return [response['content']]

