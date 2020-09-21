"""
Module to handle UI requests
"""
import sys

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import api
from resources.lib import settings
from resources.lib.model import SearchItem

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

_STREAM_PROTOCOL = 'hls'
_KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])

if _KODI_VERSION_MAJOR >= 19:
    _INPUTSTREAM_PROPERTY = 'inputstream'
else:
    _INPUTSTREAM_PROPERTY = 'inputstreamaddon'


def show_video(permalink):
    """
    Show a single video (without collection) in kodi
    :param permalink: permalink id of the video
    """
    chapter_ids = api.load_chapter_ids_of_collection(permalink)
    show_chapter_video(chapter_ids[0])


def show_chapter_video(chapter_id):
    """
    Show a video that is a chapter in the collection in kodi
    :param chapter_id: id of the chapter in the collection
    """
    token = login()
    if token is not None:
        url = api.load_stream_url_of_chapter(chapter_id, token)
        play(url)


def login():
    """
    Trys to get a token from api with credentials from settings.
    Shows error message if not successfull.
    :return token or None if not successfull
    """
    (email, password) = settings.get_credentials()
    try:
        return api.get_token(email, password)
    except api.LoginError as err:
        msg = str(err)
    except Exception: # pylint: disable=broad-except
        msg = "Unexpected Error"
    dialog = xbmcgui.Dialog()
    dialog.notification('Login failed', msg, xbmcgui.NOTIFICATION_ERROR, 5000, True)
    return None


def play(url):
    """
    Starts playing a video from a stream url
    :param url: stream url
    """
    try:
        import inputstreamhelper
        is_helper = inputstreamhelper.Helper('mpd', drm='widevine')
        if is_helper.check_inputstream():
            play_item = xbmcgui.ListItem(path=url)
            play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
            play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
            play_item.setProperty(_INPUTSTREAM_PROPERTY, is_helper.inputstream_addon)
            xbmcplugin.setResolvedUrl(_HANDLE, True, play_item)
    except ImportError as err:
        xbmc.log('Failed to load inputstream helper: ' + err.message)


def list_collection(permalink):
    """
    List collection videos
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Category Contents')
    xbmcplugin.setContent(_HANDLE, 'videos')
    collection = api.load_collection(permalink)
    videos = api.load_chapters(collection.chapter_ids)
    directory_items = map(to_directory_item, videos)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)


def list_category_contents(category_id):
    """
    List contents of a category
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Category Contents')
    xbmcplugin.setContent(_HANDLE, 'videos')
    contents = api.load_category_contents(category_id)
    directory_items = map(to_directory_item, contents)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)


def search():
    """
    Show user search dialog and perform search if they enter a query
    :return:
    """
    keyboard = xbmc.Keyboard('', 'Search for', False)
    keyboard.setDefault('')
    keyboard.doModal()

    query = keyboard.getText()
    if keyboard.isConfirmed() and query:
        list_search_results(query)


def list_search_results(query):
    """
    Get search results and show them
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Search results')
    xbmcplugin.setContent(_HANDLE, 'videos')
    contents = api.get_search_results(query)
    directory_items = map(to_directory_item, contents)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.endOfDirectory(_HANDLE)


def list_categories():
    """
    List all categories
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Categories')
    xbmcplugin.setContent(_HANDLE, 'videos')
    categories = api.load_categories()
    categories.insert(0, SearchItem())
    directory_items = map(to_directory_item, categories)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.endOfDirectory(_HANDLE)


def to_directory_item(item):
    """
    Convert arbitrary item to a directory item tuple
    :param item: object any class
    :return: directory item tuple
    """
    return item.to_directory_item()
