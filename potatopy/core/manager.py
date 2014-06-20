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

        # options must be a dictionary
        if options.has_key('status'):
            # A dictionary that contains all the HTTP status codes and according reason phrases
            status_map = {
                # 1xx: Informational - Request received, continuing process
                100: 'Continue',
                101: 'Switching Protocols',
                102: 'Processing',
                # 2xx: Success - The action was successfully received, understood, and accepted
                200: 'OK',
                201: 'Created',
                202: 'Accepted',
                203: 'Non-Authoritative Information',
                204: 'No Content',
                205: 'Reset Content',
                206: 'Partial Content',
                207: 'Multi-Status',
                208: 'Already Reported',
                226: 'IM Used',
                # 3xx: Redirection - Further action must be taken in order to complete the request
                300: 'Multiple Choices',
                301: 'Moved Permanently',
                302: 'Found',
                303: 'See Other',
                304: 'Not Modified',
                305: 'Use Proxy',
                307: 'Temporary Redirect',
                308: 'Permanent Redirect',
                # 4xx: Client Error - The request contains bad syntax or cannot be fulfilled
                400: 'Bad Request',
                401: 'Unauthorized',
                402: 'Payment Required',
                403: 'Forbidden',
                404: 'Not Found',
                405: 'Method Not Allowed',
                406: 'Not Acceptable',
                407: 'Proxy Authentication Required',
                408: 'Request Timeout',
                409: 'Conflict',
                410: 'Gone',
                411: 'Length Required',
                412: 'Precondition Failed',
                413: 'Request Entity Too Large',
                414: 'Request-URI Too Long',
                415: 'Unsupported Media Type',
                416: 'Requested Range Not Satisfiable',
                417: 'Expectation Failed',
                422: 'Unprocessable Entity',
                423: 'Locked',
                424: 'Failed Dependency',
                425: 'Reserved for WebDAV advanced collections expired proposal',
                426: 'Upgrade required',
                428: 'Precondition Required',
                429: 'Too Many Requests',
                431: 'Request Header Fields Too Large',
                # 5xx: Server Error - The server failed to fulfill an apparently valid request
                500: 'Internal Server Error',
                501: 'Not Implemented',
                502: 'Bad Gateway',
                503: 'Service Unavailable',
                504: 'Gateway Timeout',
                505: 'HTTP Version Not Supported',
                506: 'Variant Also Negotiates (Experimental)',
                507: 'Insufficient Storage',
                508: 'Loop Detected',
                510: 'Not Extended',
                511: 'Network Authentication Required'
            }
     
            if status_map.has_key(options['status']):
                # String consisting of Status-Code(cast int into string) and Reason-Phrase, separated by a single space
                response_status = str(options['status']) + ' ' + status_map[options['status']]
                
                # Must not contain a message body for 204 and 304
                if (options['status'] == 204 or options['status'] == 304):
                    response_content = ''
            else:
                Logger.log(APP_LOG_DIR, 'ERROR', __name__, 'The provided HTTP status code is invalid!')
        else:
            response_status = '200 OK'

        # Return the response as a dictionary (contains 'status', headers' and 'content')
        return {'status': response_status, 'headers': response_headers, 'content': response_content}
