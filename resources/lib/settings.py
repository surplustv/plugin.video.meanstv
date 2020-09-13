"""
Addon settings module
"""
import xbmcaddon

_ADDON = xbmcaddon.Addon()


def get_credentials():
    """
    get credentials from addon settings
    :return: username and password as tuple
    """
    email = _ADDON.getSetting('email')
    password = _ADDON.getSetting('password')
    return email, password
