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


class DurationToSecondsTestCase(TestCase):

    def test_two_part_duration(self):
        self.assertEquals(duration_to_seconds("01:02"), 62)

    def test_no_duration_returns_none(self):
        self.assertEquals(duration_to_seconds("something"), None)

    def test_three_part_duration(self):
        self.assertEquals(duration_to_seconds("01:02:03"), 3723)

    def test_looks_like_duration_but_isnt_returns_none(self):
        self.assertEquals(duration_to_seconds("01:02m"), None)
