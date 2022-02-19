"""
Model classes
"""
from __future__ import absolute_import
import sys

import xbmcaddon
import xbmcgui
from resources.lib import formatting

_ADDON = xbmcaddon.Addon()
_URL = sys.argv[0]


class Collection(object):
    """
    The meta data of a collection
    """
    def __init__(self, json):
        self.id = json['id']
        self.permalink = json['permalink']
        self.title = json['title']
        self.thumb = json['main_poster_featured']
        self.description = json['description']
        self.chapter_ids = [cv['id'] for cv in json['children_videos']] if 'children_videos' in json else []

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
        url = _URL + '?show=collection&id=' + str(self.permalink)
        return url, list_item, True

    def clean_description(self):
        """
        :return: description without html markup
        """
        return formatting.clean_html(self.description)


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
        return formatting.duration_to_seconds(self.duration)

    def clean_description(self):
        """
        :return: description without html markup
        """
        return formatting.clean_html(self.description)


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
        return formatting.duration_to_seconds(self.duration)

    def clean_description(self):
        """
        :return: description without html markup
        """
        return formatting.clean_html(self.description)


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


class SearchItem(object):
    """
    Search item in listing to start search dialog
    """

    def to_directory_item(self):  # pylint: disable=no-self-use
        """
        :return: directory item tuple
        """
        search_item = xbmcgui.ListItem(label=_ADDON.getLocalizedString(30130))
        search_item.setInfo('video', {'title': _ADDON.getLocalizedString(30130)})
        # list_item.setProperty('IsPlayable', 'true')
        url = _URL + '?show=search'
        return url, search_item, True
