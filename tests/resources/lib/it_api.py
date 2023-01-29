from unittest import TestCase

from resources.lib.api import load_collection, load_chapters, get_token, load_stream_url_of_chapter, LoginError, \
    load_categories


class LoadChapterIdsForCollectionIntegrationTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        # Collection: https://means.tv/programs/latm?categoryId=20473
        collection = load_collection('latm')
        self.assertEqual(collection.id, 'latm')
        self.assertEqual(collection.title, 'Laughter Against The Machine')
        self.assertTrue(collection.thumb)
        self.assertTrue(collection.clean_description().startswith('Laughter Against The Machine'))
        self.assertEqual(collection.chapter_ids, [572685, 572684, 572683, 572680, 572686, 572681, 572688])


class LoadChapterDetailsIntegrationTestCase(TestCase):

    def test_laughter_against_the_machine(self):
        # Chapters: https://means.tv/programs/latm?categoryId=20473
        chapters = load_chapters(572687)
        self.assertEqual(len(chapters), 7)
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
