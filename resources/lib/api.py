"""
Module for all means TV api access
"""
import requests

from resources.lib import settings
from resources.lib.model import Video, Collection, ChapterVideo, Category

_MEANS_TV_BASE_URL = 'https://means.tv/api'


def load_collection(permalink):
    """
    Load collection from API
    :param permalink: permalink id of collection
    :return: mixed list of :class:`Collection` and `Video`
    """
    url = _MEANS_TV_BASE_URL + '/contents/' + permalink
    response = requests.get(url)
    return response.json()


def load_chapter_with_credentials(chapter_id):
    """
    Loading the content of a single chapter with logging in first to get stream URL
    :param chapter_id: id of single chapter
    :return: :class:`ChapterVideo`
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


def load_category_contents(category_id):
    """
    Load contents of a category
    :param category_id: id of the category
    :return: mixed list of :class:`Collection` and :class:`Video`
    """
    url = _MEANS_TV_BASE_URL + '/contents?type=category_preview&category_id=' + str(category_id)
    response = requests.get(url)
    json_list = response.json()
    return map(to_category_content, json_list)


def load_categories():
    """
    Load categories from API
    :return: list of :class:`Category`
    """
    url = _MEANS_TV_BASE_URL + '/categories'
    response = requests.get(url)
    json_list = response.json()
    return map(to_category, json_list)


def get_token():
    """
    Retrieve user token from api through logging in
    :return: token string
    """
    (email, password) = settings.get_credentials()
    url = _MEANS_TV_BASE_URL + '/sessions'
    response = requests.post(url, json={'email': email, 'password': password})
    if response.status_code >= 400:
        raise ValueError('Unexpected status code {0}'.format(str(response.status_code)))
    return response.cookies['remember_user_token']


def to_category(json):
    """
    Convert category json to :class:`Category`
    :param json: category as json
    :return: :class:`Category`
    """
    return Category(json)


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
