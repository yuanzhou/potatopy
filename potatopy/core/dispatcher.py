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

# importlib requires Python 2.7+
import importlib

from string import Template

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
    # Add module directory to Python's search path
    sys.path.insert(1, path)
    
from application.configs.constants import APP_LOG_DIR, APP_MANAGER_DIR, APP_DEFAULT_MANAGER, APP_DEFAULT_MANAGER_METHOD, SYS_CORE_DIR
from potatopy.core.common import Common

class Dispatcher(object):
    """ 
    Dispatching -- handing the request and responsibility for the response off to
    the actual Manager/method
    """     

    # The dictionary containing server environment variables
    server_env = {}

    # Constructor
    def __init__(self, environ):
        self.server_env = environ

    def run(self, manager=None, method=None):
        """ 
        Dispatch all the HTTP requests to the provided manager/method if available
        otherwise parse the PATH_INFO
        """
        if (manager and method):
            manager_module_name = manager.lower() + '_manager'
            # Only works with get requests
            method_name = 'get_' + method.lower()
            # No paramaters needed
            params = []
        else:
            # 'get' or 'post'
            request_method = self.server_env['REQUEST_METHOD'].lower()
            
            # Trim leading backslash and trailing backslash
            # PATH_INFO of localhost or yourdomain is '/'
            request_uri = self.server_env['PATH_INFO'].strip('/')
            if not request_uri:
                request_uri = APP_DEFAULT_MANAGER + '/' + APP_DEFAULT_MANAGER_METHOD

            # Lowercase requested URI
            # Think about base64 encoded string in uri
            request_uri = request_uri.lower()

            # A list that contains manager, method, and params
            uri_segments = request_uri.split('/')
            
            # Now uri_segments contains at least manager
            manager_module_name = uri_segments[0] + '_manager'

            if (len(uri_segments) >= 2):
                # HTTP request method is prefixed
                method_name = request_method + '_' + uri_segments[1]
            else:
                method_name = request_method + '_' + APP_DEFAULT_MANAGER_METHOD.lower()

            # A list contains method parameters
            params = []
            if (len(uri_segments) >= 3):
                params = uri_segments[2:]


        # str.title() tranfsers 'about_us' to 'About_Us'
        # str.capitalize() only does 'about_us' tp 'About_us'
        manager_class_name = manager_module_name.title()

        # Introduce the response dictionary (contains 'headers' and 'content')
        # Caliing dict() is slower than just the literal dictionary syntax {}
        response = {}

        # Make sure the physical manager file exists
        if not os.path.isfile(APP_MANAGER_DIR + manager_module_name + '.py'):
            # http://docs.python.org/2/library/stdtypes.html#str.format
            # str.format() is the new standard in Python 3, and should be preferred to the % formatting 
            response = Common.handle_error("The requested Manager file '%s.py' does not exist!" % manager_module_name)
        else: 
            # Dynamically import requested manager module
            # First to check if the target module exists
            try:
                # The imp package is pending deprecation in favor of importlib
                # Same as module = __import__('application.managers.' + manager_module_name)
                # Direct use of __import__() is discouraged in favor of importlib.import_module()
                module = importlib.import_module('application.managers.' + manager_module_name)
            except ImportError:
                response = Common.handle_error("Failed to import the required application manager module: %s" % manager_module_name)
                # Return the response so the rest of the code will stop executing
                return response

            try:
                # ALl names in Python are case-sensitive
                # All module attributes (function names and class names)
                # Dynamically create object instance
                obj = getattr(module, manager_class_name)()
            except AttributeError:
                response = Common.handle_error("Module object '%s' has no attribute '%s'" % (module, manager_class_name))
                # Return the response so the rest of the code will stop executing
                return response

            # Check to see if the manager has requested method
            # There is no distinction between class properties and methods in a Python class
            # A method is just a property that is callable
            if (hasattr(obj, method_name)):
                # Requested object method
                method = getattr(obj, method_name)
                # Check to see if manager has requested method
                if callable(method):
                    # The pythonic way to check empty
                    # Empty sequences(strings, lists, tuples) are false
                    # params must be a list
                    if params:
                        # response must be a dictonary contains 'content' and 'type'
                        response = method(params)
                    else:
                        response = method()
                else:
                    # http://docs.python.org/2/library/stdtypes.html#str.format
                    # str.format() is the new standard in Python 3, and should be preferred to the % formatting 
                    response = Common.handle_error("The requested Manager method '%s' is not callable!" % method_name)
            else:
                # http://docs.python.org/2/library/stdtypes.html#str.format
                # str.format() is the new standard in Python 3, and should be preferred to the % formatting 
                response = Common.handle_error("The requested Manager method '%s' does not exist in class '%s'!" % (method_name, manager_class_name))
        
        # Return the response as a dictionary (contains 'headers' and 'content')
        # The response will be used by WSGI_Starter
        return response
