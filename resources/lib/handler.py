"""
Module to handle UI requests
"""
from __future__ import absolute_import
import sys

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib import api
from resources.lib import settings
from resources.lib import login
from resources.lib import helper
from resources.lib.model import SearchItem

# Get the plugin handle as an integer number.

_HANDLE = int(sys.argv[1])
_ADDON = xbmcaddon.Addon()

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
    collection = api.load_collection(permalink)
    show_chapter_video(collection.chapter_ids[0])


def show_chapter_video(collection_id, chapter_id):
    """
    Show a video that is a chapter in the collection in kodi
    :param chapter_id: id of the chapter in the collection
    """
    helper.log('Play Chapter - ID', chapter_id)
    url = None
    try:
        url = _get_stream_url(collection_id, chapter_id)
        helper.log('Play Chapter - URL', url)
        if url:
            _play(url)
    except Exception as err: # pylint: disable=broad-except
        helper.show_error_notification(str(err), _ADDON.getLocalizedString(30120))


def _get_stream_url(collection_id, chapter_id):
    """
    Tries to get the stream url of a chapter. If first try fails, tries to re-login (stored credentials and/or dialog)
     and tries to get the url again.
    :param collection_id: content id of the collection to which the chapter belongs
    :param chapter_id: chapter id
    :return stream url or None if not successful at all
    """
    try:
        token = settings.get_token()
        return api.load_stream_url_of_chapter(collection_id, chapter_id, token)
    except api.LoginError:
        settings.set_token('')
        login.login_with_stored_credentials()
        token = settings.get_token()
        if not token:
            login.show_login_dialog()
            token = settings.get_token()
        if token:
            return api.load_stream_url_of_chapter(collection_id, chapter_id, token)
        return None


def _play(url):
    """
    Starts playing a video from a stream url
    :param url: stream url
    :raise ImportError
    """
    import inputstreamhelper # pylint: disable=import-error
    is_helper = inputstreamhelper.Helper('mpd', drm='widevine')
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=url)
        play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        play_item.setProperty(_INPUTSTREAM_PROPERTY, is_helper.inputstream_addon)
        xbmcplugin.setResolvedUrl(_HANDLE, True, play_item)
    else:
        raise RuntimeError('Inputstream check failed')


def list_collection(permalink):
    """
    List collection videos
    """
    xbmcplugin.setPluginCategory(_HANDLE, _ADDON.getLocalizedString(30121))
    xbmcplugin.setContent(_HANDLE, 'videos')
    collection = api.load_collection(permalink)
    videos = api.load_chapters(collection.id)
    for video in videos:
        if not video.description:
            video.description = collection.description
    directory_items = [v.to_directory_item() for v in videos]
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)


def list_category_contents(category_id):
    """
    List contents of a category
    """
    xbmcplugin.setPluginCategory(_HANDLE, _ADDON.getLocalizedString(30121))
    xbmcplugin.setContent(_HANDLE, 'videos')
    contents = api.load_category_contents(category_id)
    directory_items = [c.to_directory_item() for c in contents]
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)


def search():
    """
    Show user search dialog and perform search if they enter a query
    :return:
    """
    keyboard = xbmc.Keyboard('', _ADDON.getLocalizedString(30122), False)
    keyboard.setDefault('')
    keyboard.doModal()

    query = keyboard.getText()
    if keyboard.isConfirmed() and query:
        list_search_results(query)


def list_search_results(query):
    """
    Get search results and show them
    """
    xbmcplugin.setPluginCategory(_HANDLE, _ADDON.getLocalizedString(30123))
    xbmcplugin.setContent(_HANDLE, 'videos')
    contents = api.get_search_results(query)
    directory_items = [c.to_directory_item() for c in contents]
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.endOfDirectory(_HANDLE)


def list_categories():
    """
    List all categories
    """
    xbmcplugin.setPluginCategory(_HANDLE, _ADDON.getLocalizedString(30124))
    xbmcplugin.setContent(_HANDLE, 'videos')
    categories = api.load_categories()
    categories.insert(0, SearchItem())
    directory_items = [c.to_directory_item() for c in categories]
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.endOfDirectory(_HANDLE)


def delete_password():
    """
    Delete the saved password
    """
    settings.set_password('')
    helper.show_info_notification(_ADDON.getLocalizedString(30125))
