"""
Module for all means TV api access
"""
import requests

from resources.lib.model import Video, Collection, ChapterVideo, Category

_MEANS_TV_BASE_URL = 'https://means.tv/api'

class LoginError(Exception):
    """
    Raised when login fails due to invalid credentials
    """
    pass

def load_chapter_ids_of_collection(permalink):
    """
    Loads chapter IDs of collection from API
    :param permalink: permalink id of collection
    :return: list of int
    """
    url = _MEANS_TV_BASE_URL + '/contents/' + permalink
    response = requests.get(url)
    json = response.json()
    return json['chapters']


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
            print(response.text)
            try: 
                json = response.json()
            except:
                json = dict()
            if ('email' in json):
                print(json['email'])
                raise LoginError(json['email'])
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
