from unittest import TestCase

from resources.lib.api import load_chapter_ids_of_collection


class LoadChapterIdsForCollectionTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        #https://means.tv/programs/latm?categoryId=20473
        expected = [ 1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404 ]
        actual = load_chapter_ids_of_collection('latm')
        self.assertEquals(actual, expected)
