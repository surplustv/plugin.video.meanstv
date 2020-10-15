"""
Module to handle UI requests
"""
from datetime import datetime

import xbmc
import xbmcgui

from resources.lib import api
from resources.lib import settings


DIALOG_HEADING = 'Means.TV'
NOTIFICATION_LENGTH = 5000

def show_login_dialog():
    '''
    Open login dialogs for email and password and try to login with the entered credentials.
    Store token and email in addon settings when successful logged in.
    Show info notification when logged in.
    Show error notification when error occurs.
    '''
    email = _enter_email()
    if email:
        password = _enter_password()
        if password:
            token = _login(email, password)
            if token:
                settings.set_email(email)
                settings.set_login_time(datetime.now().strftime("%Y-%m-%d %H:%M"))
                settings.set_token(token)
                show_info_message('Signed in: {0}'.format(email))


def _enter_email():
    '''
    Open dialog for email address
    :return: entered email address
    '''
    old_email = settings.get_email()
    dialog = xbmc.Keyboard(old_email, 'Email')
    dialog.doModal()
    if dialog.isConfirmed():
        return dialog.getText().strip()
    return ''


def _enter_password():
    '''
    Open dialog for password
    :return: entered password
    '''
    dialog = xbmc.Keyboard('', 'Password', True)
    dialog.doModal(60000)
    if dialog.isConfirmed():
        return dialog.getText()
    return ''


def _login(email, password):
    """
    Try to get a token from api with credentials from settings.
    Show error message if not successfull.
    :return token or None if not successfull
    """
    try:
        return api.get_token(email, password)
    except api.LoginError as err:
        show_error_message(err, 'Login failed')
    except Exception: # pylint: disable=broad-except
        show_error_message('Unexpected Error', 'Login failed')
    return None


def show_logout_dialog():
    '''
    Open logout confirmation dialog.
    Reset token and email in addon settings when user confirms to logout.
    Show info notification when logged out.
    '''
    email = settings.get_email()
    if email:
        dialog = xbmcgui.Dialog()
        confirmed = dialog.yesno(DIALOG_HEADING, 'Sign out: {0}?'.format(email))
        if confirmed:
            settings.set_email('')
            settings.set_login_time('')
            settings.set_token('')
            show_info_message('Signed out')


def show_error_message(msg, title=''):
    '''
    Show an error notification with sound
    '''
    heading = DIALOG_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_ERROR, NOTIFICATION_LENGTH, True)


def show_info_message(msg, title=''):
    '''
    Show an in notification without sound
    '''
    heading = DIALOG_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_INFO, NOTIFICATION_LENGTH, False)
