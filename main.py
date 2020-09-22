"""
Kodi plugin to view means tv
"""

import sys
from urlparse import parse_qsl

# Get the plugin url in plugin:// notation.
import resources.lib.handler as handler


def router(paramstring):
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
            handler.show_chapter_video(params['id'])
        elif params['show'] == 'search':
            handler.search()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        handler.list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])

    import resources.lib.api as api
    categories = api.load_categories()
    for cat in categories:
        contents = api.load_category_contents(cat.id)
        for content in contents:
            print('MEANSTVDESC: ' + content.description.encode('utf-8'))
