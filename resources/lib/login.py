"""
Module to handle UI requests
"""
import sys

import xbmc
import xbmcgui

from resources.lib import api
from resources.lib import settings

NOTIFICATION_HEADING = 'Means.TV'

def show_login_dialog():
    email = _enter_email()
    if email:
        password = _enter_password()
        if password:
            token = _login(email, password)
            if token:
                settings.set_email(email)
                settings.set_token(token)
                show_info_message('Signed in: {0}'.format(email))

                
def _enter_email():
    old_email = settings.get_email()
    dialog = xbmc.Keyboard(old_email, 'Email')
    dialog.doModal()
    if dialog.isConfirmed():
        #TODO validate email
        return dialog.getText().strip()
    return ''


def _enter_password():
    dialog = xbmc.Keyboard('', 'Password', True)
    dialog.doModal(60000)
    if dialog.isConfirmed():
        return dialog.getText()
    return ''


def _login(email, password):
    """
    Trys to get a token from api with credentials from settings.
    Shows error message if not successfull.
    :return token or None if not successfull
    """
    try:
        return api.get_token(email, password)
    except api.LoginError as err:
        show_error_message(err, 'Login failed')
    except Exception: # pylint: disable=broad-except
        show_error_message('Unexpected Error', 'Login failed')
    return None


def show_error_message(msg, title = ''):
    heading = NOTIFICATION_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_ERROR, 5000, True)


def show_info_message(msg, title = ''):
    heading = NOTIFICATION_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(str(title), str(msg), xbmcgui.NOTIFICATION_INFO, 5000, False)