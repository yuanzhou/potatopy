import sys

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
	# Add module directory to Python's search path
    sys.path.insert(1, path)

from potatopy.core.manager import Manager

# Class names should normally use the CapWords convention.
# JS_Manager won't work since all names in Python are case-sensitive
class Js_Manager(Manager):
    def get_index(self, params=None):
        # No template variables to render
    	content = self.render_template(params[0])
        # Must be a dictionary
        options = {'type': 'application/javascript', 'content': content}
    	
    	return self.response(options)