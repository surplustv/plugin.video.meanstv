import json
import os
from __builtin__ import isinstance
from unittest import TestCase

import requests_mock

from resources.lib.api import load_collection, load_chapters, get_search_results
from resources.lib.model import ChapterVideo, Collection, Video

_LATM_CONTENTS_JSON = os.path.join(os.path.dirname(__file__), 'latm_contents.json')
_LATM_CHAPTERS_JSON = os.path.join(os.path.dirname(__file__), 'latm_chapters.json')
_SEARCH_RESULTS_1_JSON = os.path.join(os.path.dirname(__file__), 'search_results_page1.json')
_SEARCH_RESULTS_2_JSON = os.path.join(os.path.dirname(__file__), 'search_results_page2.json')
_SEARCH_RESULTS_3_JSON = os.path.join(os.path.dirname(__file__), 'search_results_page3.json')


class LoadChapterIdsForCollectionTestCase(TestCase):

    @requests_mock.Mocker()
    def test_laughter_against_the_machine(self, m):
        # https://means.tv/programs/latm?categoryId=20473
        with open(_LATM_CONTENTS_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://means.tv/api/contents/latm', json=response_json)
        collection = load_collection('latm')
        self.assertTrue(isinstance(collection, Collection))
        self.assertEquals(collection.id, 'latm')
        self.assertEquals(collection.title, 'Laughter Against The Machine')
        self.assertEquals(collection.thumb, 'https://dtsvkkjw40x57.cloudfront.net/images/programs/572687/horizontal/big_7507_2Fcatalog_image_2F572687_2FKCnCnqiQlimDLVneahyy_LATM_Thumbnails_3.png')
        self.assertTrue(collection.clean_description().startswith('Laughter Against The Machine'))
        self.assertEquals(collection.chapter_ids, [1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404])


class LoadChapterDetailsTestCase(TestCase):

    @requests_mock.Mocker()
    def test_laughter_against_the_machine(self, m):
        # https://means.tv/programs/latm?categoryId=20473
        with open(_LATM_CHAPTERS_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://means.tv/api/chapters/?ids%5B%5D=1119397&ids%5B%5D=1119398&ids%5B%5D=1119399&ids%5B%5D=1119400&ids%5B%5D=1119401&ids%5B%5D=1119402&ids%5B%5D=1119404',
                  json=response_json)
        chapters = load_chapters([1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404])
        self.assertEquals(len(chapters), 7)
        self.assertTrue(all([isinstance(c, ChapterVideo) for c in chapters]))
        self.assertEquals(chapters[0].title, 'Episode 1 - Arizona')
        self.assertEquals(chapters[0].position, 1)
        self.assertEquals(chapters[1].title, 'Episode 2 -  Chicago')
        self.assertEquals(chapters[1].position, 2)
        self.assertEquals(chapters[2].title, 'Episode 3 - Dearborn')
        self.assertEquals(chapters[2].position, 3)
        self.assertEquals(chapters[3].title, 'Episode 4 - Wisconsin')
        self.assertEquals(chapters[3].position, 4)
        self.assertEquals(chapters[4].title, 'Episode 5 - NYC & DC')
        self.assertEquals(chapters[4].position, 5)
        self.assertEquals(chapters[5].title, 'Episode 6 - New Orleans')
        self.assertEquals(chapters[5].position, 6)
        self.assertEquals(chapters[6].title, 'Episode 7 - Oakland')
        self.assertEquals(chapters[6].position, 7)


class SearchTestCase(TestCase):
    @requests_mock.Mocker()
    def test_search(self, m):
        with open(_SEARCH_RESULTS_1_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://means.tv/api/contents?search=left&page=1', json=response_json)
        with open(_SEARCH_RESULTS_2_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://means.tv/api/contents?search=left&page=2', json=response_json)
        with open(_SEARCH_RESULTS_3_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://means.tv/api/contents?search=left&page=3', json=response_json)
        search_results = get_search_results('left')
        self.assertEquals(len(search_results), 2)
        self.assertTrue(isinstance(search_results[0], Collection))
        self.assertEquals(search_results[0].title, 'Left Trigger')
        self.assertTrue(isinstance(search_results[1], Video))
        self.assertEquals(search_results[1].title, 'PIIGS')
