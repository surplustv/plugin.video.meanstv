import sys
from urlparse import parse_qsl

import requests
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_MEANS_TV_BASE_URL = 'https://means.tv/api'


class Category(object):
    def __init__(self, json):
        self.id = json["id"]
        self.title = json["title"]

    def to_directory_item(self):
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title})
        url = _url + "?action=category&id=" + str(self.id)
        return url, list_item, True


def to_category(json):
    return Category(json)


def to_directory_item(item):
    return item.to_directory_item()


def load_categories():
    url = _MEANS_TV_BASE_URL + "/categories"
    r = requests.get(url)
    json_list = r.json()
    return map(to_category, json_list)


def list_categories():
    """
    List all categories
    """
    xbmcplugin.setPluginCategory(_handle, 'Categories')
    xbmcplugin.setContent(_handle, 'videos')
    categories = load_categories()
    directory_items = map(to_directory_item, categories)
    xbmcplugin.addDirectoryItems(_handle, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)


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
    # Check the parameters passed to the plugin
    list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
