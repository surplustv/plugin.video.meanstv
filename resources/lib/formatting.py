"""
Helper module for formatting input from means TV
"""
import re

def duration_to_seconds(duration):
    """
    Convert duration string to seconds
    :param duration: as string (either 00:00 or 00:00:00)
    :return: duration in seconds :class:`int` or None if it's in the wrong format
    """
    if not re.match("^\\d\\d:\\d\\d(:\\d\\d)?$", duration):
        return None

    array = duration.split(':')
    if len(array) == 2:
        return int(array[0]) * 60 + int(array[1])
    return int(array[0]) * 3600 + int(array[1]) * 60 + int(array[2])


def strip_tags(text):
    """
    Remove html tags from text and convert a small set of html-encoded symbols
    :param text: string with html markup
    :return: text without html markup
    """
    if text:
        clean_text = re.sub('<[^<]+?>', ' ', text)
        clean_text = clean_text.strip()
        clean_text = re.sub('\\s+', ' ', clean_text.strip())
        clean_text = clean_text.replace('&amp;', '&')
        clean_text = clean_text.replace('&nbsp;', ' ')
        return clean_text
    return text
