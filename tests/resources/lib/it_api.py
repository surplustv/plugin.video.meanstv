from unittest import TestCase

from resources.lib.api import load_collection, load_chapters, get_token, load_stream_url_of_chapter, LoginError, \
    load_categories


class LoadChapterIdsForCollectionIntegrationTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        # Collection: https://means.tv/programs/latm?categoryId=20473
        collection = load_collection('latm')
        self.assertEquals(collection.id, 'latm')
        self.assertEquals(collection.title, 'Laughter Against The Machine')
        self.assertTrue(collection.thumb)
        self.assertTrue(collection.clean_description().startswith('Laughter Against The Machine'))
        self.assertEquals(collection.chapter_ids, [1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404])


class LoadChapterDetailsIntegrationTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        # Chapters: https://means.tv/programs/latm?categoryId=20473
        chapters = load_chapters([1119397, 1119398, 1119399, 1119400, 1119401, 1119402, 1119404])
        self.assertEquals(len(chapters), 7)
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


class GetTokenTestCase(TestCase):
    
    def test_raise_login_exception(self):
        # Only works if error response by means.tv is as expected
        self.assertRaises(LoginError, lambda: get_token('no@valid.cr', 'edentials'))
        self.assertRaises(LoginError, lambda: get_token('', ''))
        self.assertRaises(LoginError, lambda: get_token(None, None))
        
        
class LoadStreamUrlOfChapter(TestCase):
    
    def test_illegal_chapter(self):
        self.assertRaises(ValueError, lambda: load_stream_url_of_chapter(0, ''))
    
    def test_no_token(self):
        # Chapter: https://means.tv/programs/jposadas
        chapter = 1206515
        self.assertRaises(LoginError, lambda: load_stream_url_of_chapter(chapter, 'xxx'))
        self.assertRaises(LoginError, lambda: load_stream_url_of_chapter(chapter, ''))
        self.assertRaises(LoginError, lambda: load_stream_url_of_chapter(chapter, None))
    
    def test_old_token(self):
        # Chapter: https://means.tv/programs/jposadas
        chapter = 1206515
        old_token = 'W1szODU1NTI0XSwiJDJhJDEwJEN6VWtDSFFneWRJSzhHZUx6ak0vVWUiLCIxNTk5NDExMTI1LjE4ODkxOTUiXQ%3D%3D--bd84f8019a8dff072dc6a71a52cba035483d6331'
        self.assertRaises(LoginError, lambda: load_stream_url_of_chapter(chapter, old_token))


class LoadCategories(TestCase):

    def test_load_categories(self):
        categories = load_categories()
        self.assertGreater(len(categories), 0)
        self.assertTrue(all(category for category in categories if category.title), "All categories should have a title")
        self.assertTrue(all(category for category in categories if category.id), "All categories should have an id")
