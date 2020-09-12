"""
Module for all means TV api access
"""
import requests

from resources.lib import settings

_MEANS_TV_BASE_URL = 'https://means.tv/api'


def load_collection(permalink):
    """
    Load collection from API
    :param permalink: permalink id of collection
    :return: json content of collection
    """
    url = _MEANS_TV_BASE_URL + '/contents/' + permalink
    response = requests.get(url)
    return response.json()


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
    :return: list of chapters as json
    """
    chapters_str = '&ids[]='.join(map(str, chapters))
    url = _MEANS_TV_BASE_URL + '/chapters/?ids[]=' + chapters_str
    response = requests.get(url)
    return response.json()


def load_category_contents(category_id):
    """
    Load contents of a category
    :param category_id: id of the category
    :return: list of videos and collections as json
    """
    url = _MEANS_TV_BASE_URL + '/contents?type=category_preview&category_id=' + str(category_id)
    response = requests.get(url)
    return response.json()


def load_categories():
    """
    Load categories from API
    :return: list categories as json
    """
    url = _MEANS_TV_BASE_URL + '/categories'
    response = requests.get(url)
    return response.json()


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
