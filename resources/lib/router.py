"""
Route requests to plugin functionality
"""
from __future__ import absolute_import
try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

from resources.lib import handler
from resources.lib import login


def route(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    if params:
        if params['show'] == 'category':
            handler.list_category_contents(params['id'])
        elif params['show'] == 'collection':
            handler.list_collection(params['id'])
        elif params['show'] == 'video':
            handler.show_video(params['id'])
        elif params['show'] == 'chapter_video':
            handler.show_chapter_video(params['coll'], params['id'])
        elif params['show'] == 'search':
            handler.search()
        elif params['show'] == 'login':
            login.show_login_dialog()
        elif params['show'] == 'logout':
            login.show_logout_dialog()
        elif params['show'] == 'delete_password':
            handler.delete_password()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        handler.list_categories()
