##############################################################################
#
# Copyright (c) 2013-2014 Zhou Yuan <yuanzhou19@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT license at
# http://www.opensource.org/licenses/mit-license.php
#
##############################################################################

import sys

import time

import logging

# The path of the root package - the root of the hierarchy of packages
# This isn't really a package, since it doesn't have an __init__.py file
path = '/Library/WebServer/Documents/potatopy'
# sys.path is just a regular Python list
if path not in sys.path:
    # Add module directory to Python's search path
    sys.path.insert(1, path)
    
from application.configs.constants import APP_LOG_DIR, APP_LOGGING_LEVEL_THRESHOLD

class Logger(object):
    """ A light, permissions-checking logging class """

    @staticmethod
    def log(dir, level, module_name, msg):
        # Dictionary of logging levels with numeric values
        levels = {
                'CRITICAL': 50,
                'ERROR': 40,
                'WARNING': 30,
                'INFO': 20,
                'DEBUG': 10
                }
        
        # Only create log file if provided level >= the threshold
        # Otherwise do nothing
        if (levels[level.upper()] >= levels[APP_LOGGING_LEVEL_THRESHOLD.upper()]):
            # The current module name
            logger = logging.getLogger(module_name)

            # Log file path and name, dir must be writable
            log_file = dir + 'potatopy_' + time.strftime("%m-%d-%Y") + '.log'
            # Make log_file writable
            file = open(log_file, 'w+')
            file.close()

            # Create a file handler
            handler = logging.FileHandler(log_file)
            
            # asctime - Default form '2003-07-08 16:49:45,896' (the numbers after the comma are millisecond portion of the time)
            # name - Name of the logger used to log the call.
            # levelname - Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
            # message - The logged message
            # More LogRecord attributes: http://docs.python.org/2/library/logging.html#logrecord-attributes
            format = '%(asctime)s - %(name)s - %(levelname)s -> %(message)s'
            # Create a logging format
            formatter = logging.Formatter(format)
            
            handler.setFormatter(formatter)
            
            # Adds the specified handler hdlr to this logger.
            logger.addHandler(handler) 
            
            # Logging levels: CRITICAL > ERROR > WARNING > INFO > DEBUG
            # Return the value for key if key is in the dictionary, else default.
            # Use a dictionary to replace switch/case statement (Python doesn't have)
            logging_level_threshold = {
                            'CRITICAL': logging.CRITICAL,
                            'ERROR': logging.ERROR,
                            'WARNING': logging.WARNING,
                            'INFO': logging.INFO,
                            'DEBUG': logging.DEBUG
                            }.get(APP_LOGGING_LEVEL_THRESHOLD.upper(), logging.DEBUG)

            # Sets the threshold for this logger lvl
            # Logging messages which are less severe than lvl will be ignored.
            logger.setLevel(logging_level_threshold)

            # Logs a message with the desired logging level on this logger.
            logging_level = {
                            'CRITICAL': 'critical',
                            'ERROR': 'error',
                            'WARNING': 'warning',
                            'INFO': 'info',
                            'DEBUG': 'debug'
                            }.get(level.upper(), 'debug')
            
            # Call the corresponding log function
            getattr(logger, logging_level)(msg)
