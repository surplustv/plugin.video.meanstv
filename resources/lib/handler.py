"""
Module to handle UI requests
"""
import sys

import xbmc
import xbmcgui
import xbmcplugin

import resources.lib.api as api
from resources.lib.model import Category, Video, Collection, ChapterVideo

# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

_STREAM_PROTOCOL = 'hls'
_KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])

if _KODI_VERSION_MAJOR >= 19:
    _INPUTSTREAM_PROPERTY = 'inputstream'
else:
    _INPUTSTREAM_PROPERTY = 'inputstreamaddon'


def to_category(json):
    """
    Convert category json to :class:`Category`
    :param json: category as json
    :return: :class:`Category`
    """
    return Category(json)


def to_directory_item(item):
    """
    Convert arbitrary item to a directory item tuple
    :param item: object any class
    :return: directory item tuple
    """
    return item.to_directory_item()


def to_category_content(item):
    """
    Conver json list item from category content to video or collection
    :param item: category content item (json)
    :return: depending on content type :class:`Video` and :class:`Collection`
    """
    content_type = item['content_type']
    if content_type == 'video':
        return Video(item)
    return Collection(item)


def to_chapter_video(json):
    """
    Convert json to :class:`ChapterVideo`
    :param json: map of json content
    :return: :class:`ChapterVideo`
    """
    return ChapterVideo(json)


def show_chapter_video(chapter_id):
    """
    Show a video that is a chapter in the collection in kodi
    :param chapter_id: id of the chapter in the collection
    """
    chapter = api.load_chapter_with_credentials(chapter_id)
    url = chapter['subject']['versions']['hls']
    try:
        import inputstreamhelper
        is_helper = inputstreamhelper.Helper('mpd', drm='widevine')
        if is_helper.check_inputstream():
            play_item = xbmcgui.ListItem(path=url)
            play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
            play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
            play_item.setProperty(_INPUTSTREAM_PROPERTY, is_helper.inputstream_addon)
            xbmcplugin.setResolvedUrl(_HANDLE, True, play_item)
    except ImportError as exception:
        xbmc.log('Failed to load inputstream helper: ' + exception.message)


def show_video(permalink):
    """
    Show a single video (without collection) in kodi
    :param permalink: permalink id of the video
    """
    collection = api.load_collection(permalink)
    show_chapter_video(collection['chapters'][0])


def list_collection(permalink):
    """
    List collection videos
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Category Contents')
    xbmcplugin.setContent(_HANDLE, 'videos')
    collection = api.load_collection(permalink)
    json_list = api.load_chapters(collection['chapters'])
    videos = map(to_chapter_video, json_list)
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
    json_list = api.load_category_contents(category_id)
    contents = map(to_category_content, json_list)
    directory_items = map(to_directory_item, contents)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)


def list_categories():
    """
    List all categories
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Categories')
    xbmcplugin.setContent(_HANDLE, 'videos')
    json_list = api.load_categories()
    categories = map(to_category, json_list)
    directory_items = map(to_directory_item, categories)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)
