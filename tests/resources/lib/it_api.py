from __builtin__ import isinstance
from unittest import TestCase

from resources.lib.api import load_chapter_ids_of_collection, load_chapters
from resources.lib.model import ChapterVideo


class LoadChapterIdsForCollectionIntegrationTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        # https://means.tv/programs/latm?categoryId=20473
        expected = [1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404]
        actual = load_chapter_ids_of_collection('latm')
        self.assertEquals(actual, expected)


class LoadChapterDetailsIntegrationTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        # https://means.tv/programs/latm?categoryId=20473
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
