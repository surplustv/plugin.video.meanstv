"""
Kodi plugin to view means tv
"""

import re
import sys
from urlparse import parse_qsl

import requests
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# Get the plugin url in plugin:// notation.
from bs4 import BeautifulSoup

_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

_STREAM_PROTOCOL = 'hls'
_MEANS_TV_BASE_URL = 'https://means.tv/api'
_KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])
_ADDON = xbmcaddon.Addon()

if _KODI_VERSION_MAJOR >= 19:
    _INPUTSTREAM_PROPERTY = 'inputstream'
else:
    _INPUTSTREAM_PROPERTY = 'inputstreamaddon'


class Category(object):
    """
    Main category from the start page
    """

    def __init__(self, json):
        self.id = json['id']
        self.title = json['title']

    def to_directory_item(self):
        """
        :return: directory item tuple
        """
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title})
        url = _URL + '?show=category&id=' + str(self.id)
        return url, list_item, True


class Video(object):
    """
    A single video that is not part of any collection
    """

    def __init__(self, json):
        self.id = json['permalink']
        self.title = json['title']
        self.thumb = json['main_poster_featured']
        self.duration = json['duration']
        self.description = json['description']

    def to_directory_item(self):
        """
        :return: directory item tuple
        """
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title,
                                    'plot': self.clean_description(),
                                    'duration': self.duration_to_seconds()})
        list_item.setArt({'thumb': self.thumb,
                          'icon': self.thumb,
                          'fanart': self.thumb})
        list_item.setProperty('IsPlayable', 'true')
        url = _URL + '?show=video&id=' + str(self.id)
        return url, list_item, False

    def duration_to_seconds(self):
        """
        :return: duration in seconds
        """
        return duration_to_seconds(self.duration)

    def clean_description(self):
        """
        :return: description without html markup
        """
        return strip_tags(self.description)


class ChapterVideo(object):
    """
    The video chapter of a collection
    """

    def __init__(self, json):
        self.id = json['id']
        self.position = json['position']
        self.title = json['title']
        self.thumb = json['preview_image']
        self.duration = json['subject']['duration']
        self.description = json['description']

    def to_directory_item(self):
        """
        :return: directory item tuple
        """
        title = str(self.position) + ". " + self.title
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title,
                                    'plot': self.clean_description(),
                                    'duration': self.duration_to_seconds()})
        list_item.setArt({'thumb': self.thumb,
                          'icon': self.thumb,
                          'fanart': self.thumb})
        list_item.setProperty('IsPlayable', 'true')
        url = _URL + '?show=chapter_video&id=' + str(self.id)
        return url, list_item, False

    def duration_to_seconds(self):
        """
        :return: duration in seconds
        """
        return duration_to_seconds(self.duration)

    def clean_description(self):
        """
        :return: description without html markup
        """
        return strip_tags(self.description)


class Collection(object):
    """
    The meta data of a collection
    """
    def __init__(self, json):
        self.id = json['permalink']
        self.title = json['title']
        self.thumb = json['main_poster_featured']
        self.description = json['description']

    def to_directory_item(self):
        """
        :return: directory item tuple
        """
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title,
                                    'plot': self.clean_description()})
        list_item.setArt({'thumb': self.thumb,
                          'icon': self.thumb,
                          'fanart': self.thumb})
        url = _URL + '?show=collection&id=' + str(self.id)
        return url, list_item, True

    def clean_description(self):
        """
        :return: description without html markup
        """
        return strip_tags(self.description)


def duration_to_seconds(duration):
    """
    Convert duration string to seconds
    :param duration: as string (either 00:00 or 00:00:00)
    :return: duration in seconds :class:`int`
    """
    array = duration.split(':')
    if len(array) == 2:
        return int(array[0]) * 60 + int(array[1])
    return int(array[0]) * 3600 + int(array[1]) * 60 + int(array[2])


def strip_tags(text):
    """
    Remove tags from text
    :param text: string with html markup
    :return: text without html markup
    """
    if text:
        clean_text = BeautifulSoup(text, features='html.parser').get_text(separator=' ')
        return re.sub('\\s+', ' ', clean_text)
    return text


def to_category(json):
    """
    Convert category json to :class:`Category`
    :param json: category as json
    :return: :class:`Category`
    """
    return Category(json)


def to_directory_item(item):
    return item.to_directory_item()


def load_categories():
    """
    Load categories from API
    :return: list :class:`Category`
    """
    url = _MEANS_TV_BASE_URL + '/categories'
    response = requests.get(url)
    json_list = response.json()
    return map(to_category, json_list)


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


def load_category_contents(category_id):
    """
    Load contents of a category
    :param category_id: id of the category
    :return: mixed list of :class:`Video` and :class:`Collection`
    """
    url = _MEANS_TV_BASE_URL + '/contents?type=category_preview&category_id=' + str(category_id)
    response = requests.get(url)
    json_list = response.json()
    return map(to_category_content, json_list)


def load_collection(permalink):
    """
    Load collection from API
    :param permalink: permalink id of collection
    :return: json content of collection
    """
    url = _MEANS_TV_BASE_URL + '/contents/' + permalink
    response = requests.get(url)
    return response.json()


def to_chapter_video(json):
    """
    Convert json to :class:`ChapterVideo`
    :param json: map of json content
    :return: :class:`ChapterVideo`
    """
    return ChapterVideo(json)


def load_chapter_with_credentials(chapter_id):
    """
    Loading the content of a single chapter with logging in first to get stream URL
    :param chapter_id: id of single chapter
    :return: json content of chapter
    """
    url = _MEANS_TV_BASE_URL + '/chapters/?ids[]=' + str(chapter_id)
    cookies = {'remember_user_token': get_token()}
    response = requests.get(url, cookies=cookies)
    return response.json()[0]


def load_chapters(chapters):
    """
    load the chapter details from the API without being logged in
    :param chapters: list of chapter ids
    :return: list of :class:`ChapterVideo`
    """
    chapters_str = '&ids[]='.join(map(str, chapters))
    url = _MEANS_TV_BASE_URL + '/chapters/?ids[]=' + chapters_str
    response = requests.get(url)
    json_list = response.json()
    return map(to_chapter_video, json_list)


def show_chapter_video(chapter_id):
    """
    Show a video that is a chapter in the collection in kodi
    :param chapter_id: id of the chapter in the collection
    """
    chapter = load_chapter_with_credentials(chapter_id)
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
    collection = load_collection(permalink)
    show_chapter_video(collection['chapters'][0])


def list_collection(permalink):
    """
    List collection videos
    """
    xbmcplugin.setPluginCategory(_HANDLE, 'Category Contents')
    xbmcplugin.setContent(_HANDLE, 'videos')
    collection = load_collection(permalink)
    videos = load_chapters(collection['chapters'])
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
    contents = load_category_contents(category_id)
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
    categories = load_categories()
    directory_items = map(to_directory_item, categories)
    xbmcplugin.addDirectoryItems(_HANDLE, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_HANDLE)


def get_credentials():
    """
    get credentials from addon settings
    :return: username and password as tuple
    """
    email = _ADDON.getSetting('email')
    password = _ADDON.getSetting('password')
    return email, password


def get_token():
    """
    Retrieve user token from api through logging in
    :return: token string
    """
    (email, password) = get_credentials()
    url = _MEANS_TV_BASE_URL + '/sessions'
    response = requests.post(url, json={'email': email, 'password': password})
    if response.status_code >= 400:
        raise ValueError('Unexpected status code {0}'.format(str(response.status_code)))
    return response.cookies['remember_user_token']


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
            list_category_contents(params['id'])
        elif params['show'] == 'collection':
            list_collection(params['id'])
        elif params['show'] == 'video':
            show_video(params['id'])
        elif params['show'] == 'chapter_video':
            show_chapter_video(params['id'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
