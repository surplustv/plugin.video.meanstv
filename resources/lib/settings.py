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

def get_email():
    """
    get email from addon settings
    :return: email
    """
    return _ADDON.getSetting('email')

def set_email(email):
    """
    set email in addon settings
    :param: email: new email address
    """
    return _ADDON.setSetting('email', email)

def get_token():
    """
    get remember_user_token from addon settings
    :return: token
    """
    return _ADDON.getSetting('remember_user_token')

def set_token(token):
    """
    set remember_user_token in addon settings
    :param: token: new token
    """
    return _ADDON.setSetting('remember_user_token', token)
