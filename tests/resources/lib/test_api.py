import json
import os
from builtins import isinstance
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
            m.get('https://api-u-alpha.global.ssl.fastly.net/api/contents/latm', json=response_json)
        collection = load_collection('latm')
        self.assertTrue(isinstance(collection, Collection))
        self.assertEqual(collection.id, 572687)
        self.assertEqual(collection.title, 'Laughter Against The Machine')
        self.assertEqual(collection.thumb, 'https://alpha.uscreencdn.com/images/programs/572687/horizontal/big_7507_2Fcatalog_image_2F572687_2FE6uopBSAQHKqm91hLvyG_LATM_20ORIGINAL_20CORNER_202.jpg')
        self.assertTrue(collection.clean_description().startswith('Laughter Against The Machine'))
        self.assertEqual(collection.chapter_ids, [572685, 572684, 572683, 572680, 572686, 572681, 572688])


class LoadChapterDetailsTestCase(TestCase):

    @requests_mock.Mocker()
    def test_laughter_against_the_machine(self, m):
        # https://means.tv/programs/latm?categoryId=20473
        with open(_LATM_CHAPTERS_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://api-u-alpha.global.ssl.fastly.net/api/chapters/?content_id=%5B1119397,%201119398,%201119399,%201119400,%201119401,%201119402,%201119404,%201711409%5D',
                  json=response_json)
        chapters = load_chapters([1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404, 1711409])
        self.assertEqual(len(chapters), 7)
        self.assertTrue(all([isinstance(c, ChapterVideo) for c in chapters]))
        self.assertEqual(chapters[0].title, 'Episode 1 - Arizona')
        self.assertEqual(chapters[0].position, 1)
        self.assertEqual(chapters[1].title, 'Episode 2 -  Chicago')
        self.assertEqual(chapters[1].position, 2)
        self.assertEqual(chapters[2].title, 'Episode 3 - Dearborn')
        self.assertEqual(chapters[2].position, 3)
        self.assertEqual(chapters[3].title, 'Episode 4 - Wisconsin')
        self.assertEqual(chapters[3].position, 4)
        self.assertEqual(chapters[4].title, 'Episode 5 - NYC & DC')
        self.assertEqual(chapters[4].position, 5)
        self.assertEqual(chapters[5].title, 'Episode 6 - New Orleans')
        self.assertEqual(chapters[5].position, 6)
        self.assertEqual(chapters[6].title, 'Episode 7 - Oakland')
        self.assertEqual(chapters[6].position, 7)


class SearchTestCase(TestCase):
    @requests_mock.Mocker()
    def test_search(self, m):
        with open(_SEARCH_RESULTS_1_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://api-u-alpha.global.ssl.fastly.net/api/contents?search=left&page=1', json=response_json)
        with open(_SEARCH_RESULTS_2_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://api-u-alpha.global.ssl.fastly.net/api/contents?search=left&page=2', json=response_json)
        with open(_SEARCH_RESULTS_3_JSON, "r") as response_file:
            response_json = json.load(response_file)
            m.get('https://api-u-alpha.global.ssl.fastly.net/api/contents?search=left&page=3', json=response_json)
        search_results = get_search_results('left')
        self.assertEqual(len(search_results), 2)
        self.assertTrue(isinstance(search_results[0], Collection))
        self.assertEqual(search_results[0].title, 'Left Trigger')
        self.assertTrue(isinstance(search_results[1], Video))
        self.assertEqual(search_results[1].title, 'PIIGS')
