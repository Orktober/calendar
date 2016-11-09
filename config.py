'''
Env-aware configuration for the scheduler.

This config.py is a common file that I have used in many applications.  It has
been very effective at abstracting where exactly configuration details come
from.

Typically, shared configs are checked into yaml config files, while sensitive or
machine-dependent configurations come from either a private.yml file placed on
the server (not tracked in version control), or from a sourced config.sh file.

This file will detect configurations coming from any of those sources.
'''
import os
import sys
import yaml
import pymongo
import logging

# The app will only accept recognized environments
VALID_ENVS  = ['devel', 'staging', 'prod']


# Don't bring up the app if the env is not explicitly set
try:
    env = os.environ['ENV']
except KeyError as e:
    print('FATAL - app misconfigured - no ENV variable set')
    sys.exit(-1)


# Restrict what env the app can come up in to predefined values
if env not in VALID_ENVS:
    print('FATAL - app misconfigured - ENV {0} is not recognized'.format(env))


if env == 'devel':
    level = logging.DEBUG
else:
    level = logging.INFO

# Set up logging
logging.basicConfig(level=level)
log = logging.getLogger(__name__)


def load_config_from_env(config):
    ''' Util to pull config vars from the environment '''
    for key, val in os.environ.items():
        config[key] = val


def merge_config(left, right):
    '''Merges the right-hand config ainto the left-hand config,

    Merges are performed with the following logic:
        Non-dict objects with the same key:
            - the value on the RHS is preferred
        Dict objects:
            - all values from LHS are merged into existing RHS
    '''
    for key, val in right.items():
        if key in left and isinstance(left[key], dict) and isinstance(val, dict):
            left[key] = merge_config(left[key], val)
        else:
            left[key] = val
    return left


# Find the config file for this env and load it (eg config/devel.yml')
_here = os.path.dirname(os.path.abspath(__file__))
_config_file = open(os.path.join(_here, 'config/{env}.yml'.format(env=env)), 'r')
config = yaml.load(_config_file)


# Attempt to load a private config file - this may or may not be present
try:
    _private_file = open(os.path.join(_here, 'config/private.yml'), 'r')
    merge_config(config, yaml.load(_private_file))
except FileNotFoundError as e:
    log.debug("private.yml file not found - skipping")


# Pull the environment config into the app
load_config_from_env(config)
