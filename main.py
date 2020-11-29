"""
Kodi plugin to view means tv
"""
from __future__ import absolute_import
import sys

from resources.lib import router

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router.route(sys.argv[2][1:])
