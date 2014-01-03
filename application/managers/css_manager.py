import sys

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
	# Add module directory to Python's search path
    sys.path.insert(1, path)

from application.configs.constants import STATIC_URI_BASE
from potatopy.core.manager import Manager

# Class names should normally use the CapWords convention.
# CSS_Manager won't work since all names in Python are case-sensitive
class Css_Manager(Manager):
    def get_index(self, params=None):
        # Must be a dictionary
        template_vars = {'STATIC_URI_BASE': STATIC_URI_BASE}
    	content = self.render_template(params[0], template_vars)
        # Must be a dictionary
        options = {'type': 'text/css; charset=utf-8', 'content': content}
    	
    	return self.response(options)