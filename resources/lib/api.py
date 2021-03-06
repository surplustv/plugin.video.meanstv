"""
Module for all means TV api access
"""
from __future__ import absolute_import
import requests

from resources.lib.model import Video, Collection, ChapterVideo, Category

_FASTLY_ORIGIN_HEADER = 'X-Fastly-Origin'
_FASTLY_ORIGIN_HEADER_VALUE = 'meansmediatv'
_MEANS_TV_BASE_URL = 'https://means.tv/api'


class LoginError(Exception):
    """
    Raised when login fails due to invalid credentials
    """
    pass


class ApiError(Exception):
    """
    Raised when the API behaves in some unexpected way
    """
    pass


def load_collection(permalink):
    """
    Loads a single collection from API
    :param permalink: permalink id of collection
    :return: :class: `Collection`
    """
    url = _MEANS_TV_BASE_URL + '/contents/' + permalink
    response = requests.get(url)
    json = response.json()
    return Collection(json)


def load_stream_url_of_chapter(chapter_id, token):
    """
    Loads the stream URL of a single chapter while being logged in
    :param chapter_id: id of single chapter
    :param token: login token
    :return: str
    """
    url = _MEANS_TV_BASE_URL + '/chapters/?ids[]=' + str(chapter_id)
    cookies = {'remember_user_token': token}
    response = requests.get(url, cookies=cookies)
    json = response.json()
    if not json:
        raise ValueError('Chapter {0} not found.'.format(str(chapter_id)))
    if not json[0]['has_access']:
        raise LoginError('Access denied to chapter {0}'.format(str(chapter_id)))
    if not json[0]['subject']['versions']['hls']:
        raise ValueError('No stream url found for chapter {0}'.format(str(chapter_id)))
    return json[0]['subject']['versions']['hls']


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
    return [ChapterVideo(item) for item in json_list if item['chapter_type'] == 'video']


def load_category_contents(category_id):
    """
    Load contents of a category
    :param category_id: id of the category
    :return: mixed list of :class:`Collection` and :class:`Video`
    """
    url = _MEANS_TV_BASE_URL + '/contents?type=category_preview&category_id=' + str(category_id)
    response = requests.get(url)
    json_list = response.json()
    return [to_category_content(item) for item in json_list]


def load_categories():
    """
    Load categories from API
    :return: list of :class:`Category`
    """
    url = _MEANS_TV_BASE_URL + '/categories'
    response = requests.get(url, headers={_FASTLY_ORIGIN_HEADER: _FASTLY_ORIGIN_HEADER_VALUE})
    json_list = response.json()
    return [Category(item) for item in json_list]


def get_search_results(query):
    """
    Get search results for a query
    :param query: search term
    :return: list of :class:`Collection` or :class:`Video`
    """
    results = []
    page = 1
    results_for_page = _get_search_results_for_page(query, page)
    while results_for_page:
        results.extend(results_for_page)
        page += 1
        results_for_page = _get_search_results_for_page(query, page)
    return [to_category_content(item) for item in results]


def _get_search_results_for_page(query, page):
    """
    Get search results for a query and a specific page
    :param query: search term
    :param page: page number of search results
    :return: list of json
    """
    params = {'search': query, 'page': page}
    url = _MEANS_TV_BASE_URL + '/contents'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return ApiError("API returned unknown status code: {0}".format(response.status_code))


def get_token(email, password):
    """
    Retrieve user token from API through logging in
    :param email: login email address
    :param password: login password
    :return: token string
    :raises LoginError: when login failed due to invalid credentials
    :raises ValueError: when an unexpected status code is returned by API
    """
    url = _MEANS_TV_BASE_URL + '/sessions'
    response = requests.post(url, json={'email': email, 'password': password})
    if response.status_code >= 400:
        if response.status_code == 422:
            try:
                json = response.json()
            except ValueError:
                json = dict()
            if ('email' in json and isinstance(json['email'], list) and json['email']):
                raise LoginError(json['email'][0])
        raise ValueError('Unexpected status code {0}'.format(str(response.status_code)))
    return response.cookies['remember_user_token']


def to_category_content(item):
    """
    Conver json list item from category content to video or collection
    :param item: category content item (json)
    :return: depending on content type :class:`Video` and :class:`Collection`
    """
    if item['content_type'] == 'video':
        return Video(item)
    return Collection(item)
