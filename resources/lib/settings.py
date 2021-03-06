"""
Addon settings module
"""
from __future__ import absolute_import
import xbmcaddon

_ADDON = xbmcaddon.Addon()

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

def get_login_time():
    """
    get time of active login from addon settings
    :return: login time as formatted string
    """
    return _ADDON.getSetting('login_time')

def set_login_time(time):
    """
    set time of active login in addon settings
    :param: time: login time as formatted string
    """
    return _ADDON.setSetting('login_time', time)

def get_password():
    """
    get saved password for login
    """
    return _ADDON.getSetting('password')

def set_password(password):
    """
    set password for login
    :param: password: password for login
    """
    return _ADDON.setSetting('password', password)
