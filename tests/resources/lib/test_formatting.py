from unittest import TestCase

from resources.lib.formatting import strip_tags, duration_to_seconds


class StripTagsTestCase(TestCase):

    def test_for_none_returns_none(self):
        self.assertEquals(strip_tags(None), None)

    def test_for_empty_string_returns_empty_string(self):
        self.assertEquals(strip_tags(""), "")

    def test_without_tags_returns_same_string(self):
        self.assertEquals(strip_tags("No tags at all"), "No tags at all")

    def test_with_tags_returns_string_without_tags(self):
        self.assertEquals(strip_tags("<p>something</p>"), "something")

    def test_with_tags_returns_string_without_tags_separates_by_single_space(self):
        self.assertEquals(strip_tags("<h1>headline</h1><p>something <b>with</b> <i>tags</i></p>"),
                          "headline something with tags")

    def test_longer_real_world_text(self):
        self.assertEquals(strip_tags("<p><strong><em>Laughter Against The Machine</em></strong> is a seven part documentary series following comedians W. Kamau Bell, Nato Green, and Janine Brito as they journey across the U.S. in 2011 before and after Occupy protests rock the nation.</p><p>The trio visits some of the least funny places in the world, like the militarized US/Mexico border, the 9th Ward in New Orleans that was devastated by Hurricane Katrina, or Oakland under martial law during Occupy. Amidst this grim political backdrop, the comics try and help their audiences unwind between being teargassed by cops or arrested for blocking ICE deportations.</p><p><br></p><p>Released in 2020</p>"),
                          "Laughter Against The Machine is a seven part documentary series following comedians W. Kamau Bell, Nato Green, and Janine Brito as they journey across the U.S. in 2011 before and after Occupy protests rock the nation. The trio visits some of the least funny places in the world, like the militarized US/Mexico border, the 9th Ward in New Orleans that was devastated by Hurricane Katrina, or Oakland under martial law during Occupy. Amidst this grim political backdrop, the comics try and help their audiences unwind between being teargassed by cops or arrested for blocking ICE deportations. Released in 2020")


class DurationToSecondsTestCase(TestCase):

    def test_two_part_duration(self):
        self.assertEquals(duration_to_seconds("01:02"), 62)

    def test_no_duration_returns_none(self):
        self.assertEquals(duration_to_seconds("something"), None)

    def test_three_part_duration(self):
        self.assertEquals(duration_to_seconds("01:02:03"), 3723)

    def test_looks_like_duration_but_isnt_returns_none(self):
        self.assertEquals(duration_to_seconds("01:02m"), None)
