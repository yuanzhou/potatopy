import sys

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
    # Add module directory to Python's search path
    sys.path.insert(1, path)
    
from application.configs.constants import APP_URI_BASE, STATIC_URI_BASE
from potatopy.core.manager import Manager

# Class names should normally use the CapWords convention.
class Home_Manager(Manager):
    # Function names should be lowercase, with words separated by underscores as necessary to improve readability.
    # Don't use spaces around the = sign when used to indicate a keyword argument or a default parameter value.
    # We don't use the term "private" here, since no attribute is really private in Python 
    def get_index(self, params=None):
        # Must be a dictionary
        template_vars = {'APP_URI_BASE': APP_URI_BASE, 'STATIC_URI_BASE': STATIC_URI_BASE, 'page_title': 'Home'}
    	content = self.render_template('home_index.html', template_vars)
        # Must be a dictionary
        options = {'type': 'text/html; charset=utf-8', 'content': content}
    	
    	return self.response(options)