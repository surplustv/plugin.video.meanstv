import re
import sys
from urlparse import parse_qsl

import requests
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
from bs4 import BeautifulSoup

_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_MEANS_TV_BASE_URL = 'https://means.tv/api'


class Category(object):
    def __init__(self, json):
        self.id = json['id']
        self.title = json['title']

    def to_directory_item(self):
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title})
        url = _url + '?show=category&id=' + str(self.id)
        return url, list_item, True


class Video(object):
    def __init__(self, json):
        self.id = json['permalink']
        self.title = json['title']
        self.thumb = json['main_poster_featured']
        self.duration = json['duration']
        self.description = json['description']

    def to_directory_item(self):
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title,
                                    'plot': self.clean_description(),
                                    'duration': self.duration_to_seconds()})
        list_item.setArt({'thumb': self.thumb,
                          'icon': self.thumb,
                          'fanart': self.thumb})
        url = _url + '?show=video&id=' + str(self.id)
        return url, list_item, False

    def duration_to_seconds(self):
        return duration_to_seconds(self.duration)

    def clean_description(self):
        return strip_tags(self.description)


class ChapterVideo(object):
    def __init__(self, json):
        self.id = json['id']
        self.position = json['position']
        self.title = json['title']
        self.thumb = json['preview_image']
        self.duration = json['subject']['duration']
        self.description = json['description']

    def to_directory_item(self):
        title = str(self.position) + ". " + self.title
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title,
                                    'plot': self.clean_description(),
                                    'duration': self.duration_to_seconds()})
        list_item.setArt({'thumb': self.thumb,
                          'icon': self.thumb,
                          'fanart': self.thumb})
        url = _url + '?show=chapter_video&id=' + str(self.id)
        return url, list_item, False

    def duration_to_seconds(self):
        return duration_to_seconds(self.duration)

    def clean_description(self):
        return strip_tags(self.description)


class Collection(object):
    def __init__(self, json):
        self.id = json['permalink']
        self.title = json['title']
        self.thumb = json['main_poster_featured']
        self.description = json['description']

    def to_directory_item(self):
        list_item = xbmcgui.ListItem(label=self.title)
        list_item.setInfo('video', {'title': self.title,
                                    'plot': self.clean_description()})
        list_item.setArt({'thumb': self.thumb,
                          'icon': self.thumb,
                          'fanart': self.thumb})
        url = _url + '?show=collection&id=' + str(self.id)
        return url, list_item, True

    def clean_description(self):
        return strip_tags(self.description)


def duration_to_seconds(duration):
    array = duration.split(':')
    if len(array) == 2:
        return int(array[0]) * 60 + int(array[1])
    else:
        return int(array[0]) * 3600 + int(array[1]) * 60 + int(array[2])


def strip_tags(text):
    if text:
        clean_text = BeautifulSoup(text, features='html.parser').get_text(separator=' ')
        return re.sub('\\s+', ' ', clean_text)
    else:
        return text


def to_category(json):
    return Category(json)


def to_directory_item(item):
    return item.to_directory_item()


def load_categories():
    url = _MEANS_TV_BASE_URL + '/categories'
    r = requests.get(url)
    json_list = r.json()
    return map(to_category, json_list)


def to_category_content(item):
    content_type = item['content_type']
    if content_type == 'video':
        return Video(item)
    else:
        return Collection(item)


def load_category_contents(category_id):
    url = _MEANS_TV_BASE_URL + '/contents?type=category_preview&category_id=' + str(category_id)
    r = requests.get(url)
    json_list = r.json()
    return map(to_category_content, json_list)


def load_collection(permalink):
    url = _MEANS_TV_BASE_URL + '/contents/' + permalink
    r = requests.get(url)
    return r.json()


def to_chapter_video(json):
    return ChapterVideo(json)


def load_chapters(chapters):
    chapters_str = '&ids[]='.join(map(str, chapters))
    url = _MEANS_TV_BASE_URL + '/chapters/?ids[]=' + chapters_str
    r = requests.get(url)
    json_list = r.json()
    return map(to_chapter_video, json_list)


def list_collection(permalink):
    """
    List collection videos
    """
    xbmcplugin.setPluginCategory(_handle, 'Category Contents')
    xbmcplugin.setContent(_handle, 'videos')
    collection = load_collection(permalink)
    videos = load_chapters(collection['chapters'])
    directory_items = map(to_directory_item, videos)
    xbmcplugin.addDirectoryItems(_handle, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)


def list_category_contents(category_id):
    """
    List contents of a category
    """
    xbmcplugin.setPluginCategory(_handle, 'Category Contents')
    xbmcplugin.setContent(_handle, 'videos')
    contents = load_category_contents(category_id)
    directory_items = map(to_directory_item, contents)
    xbmcplugin.addDirectoryItems(_handle, directory_items, len(directory_items))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)


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
    if params:
        if params['show'] == 'category':
            list_category_contents(params['id'])
        elif params['show'] == 'collection':
            list_collection(params['id'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
