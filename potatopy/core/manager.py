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
    
from application.configs.constants import APP_LOG_DIR, APP_TEMPLATE_DIR
from potatopy.core.logger import Logger

class Manager(object):
    """ 
    The base manager class that renders the templates and
    outputs the final output
    """
    
    def render_template(self, template, template_vars=None):
        # Make sure the physical template file exists
        if not os.path.isfile(APP_TEMPLATE_DIR + template):
            # Can't use Common.handle_error() here becuse render_template() 
            # returns a string to be used by manager, while Common.handle_error() 
            # returns a response dictionary to be handled by WSGI_Starter
            Logger.log(APP_LOG_DIR, 'ERROR', __name__, 'No template file: ' + template)
            return 'No template file: ' + template
        else:    
            # No need to explicitly call f.close() since with ... as
            with open(APP_TEMPLATE_DIR + template, 'r') as f:
                template_content = f.read()
            
            # Render template variables if provided
            # Otherwise, just return the template content
            if isinstance(template_vars, dict):
                # The rendered template will be returned as a string
                # Like the substitute(), except that KeyErrors are never raised 
                # (due to placeholders missing from the mapping). 
                # When a placeholder is missing, the original placeholder 
                # will appear in the resulting string.
                # Also, unlike with substitute(), any other appearances of the $ 
                # will simply return $ instead of raising ValueError.
                return Template(template_content).safe_substitute(template_vars)
            else:
                return template_content

    def response(self, options):
        # These are HTTP headers expected by the client.
        # They must be wrapped as a list of tupled pairs:
        # [(Header name, Header value)].
        response_headers = [('Content-Type', options['type'])]

        response_content = options['content']

        # Return the response as a dictionary (contains 'headers' and 'content')
        return {'headers': response_headers, 'content': response_content}
