"""
Module to handle UI requests
"""
from __future__ import absolute_import

from datetime import datetime

import xbmc
import xbmcgui

from resources.lib import api
from resources.lib import helper
from resources.lib import settings


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
                helper.show_info_notification('Signed in: {0}'.format(email))
                if _store_password():
                    settings.set_password(password)


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
    """"
    Open dialog for password
    :return: entered password
    """
    dialog = xbmc.Keyboard('', 'Password', True)
    dialog.doModal(60000)
    if dialog.isConfirmed():
        return dialog.getText()
    return ''


def _store_password():
    """
    Open dialog to ask if password should be stored
    :return: True if it should be stored, False otherwise
    """
    dialog = xbmcgui.Dialog()
    return dialog.yesno('Save password', 'Do you want to save the password?',
                        'This is not required and not recommended as the password will be stored unencrypted. '
                        'If stored, the password will be used for automatic login, when the login token expires.')


def _login(email, password):
    """
    Try to get a token from api with credentials from settings.
    Show error message if not successfull.
    :return token or None if not successfull
    """
    try:
        return api.get_token(email, password)
    except api.LoginError as err:
        helper.show_error_notification(err, 'Login failed')
    except Exception: # pylint: disable=broad-except
        helper.show_error_notification('Unexpected Error', 'Login failed')
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
        confirmed = dialog.yesno(helper.DIALOG_HEADING, 'Sign out: {0}?'.format(email))
        if confirmed:
            settings.set_email('')
            settings.set_login_time('')
            settings.set_token('')
            settings.set_password('')
            helper.show_info_notification('Signed out')


def login_with_stored_credentials():
    """
    Try login with stored credentials, if they exist. Updates stored token on success, otherwise fails silently.
    """
    email = settings.get_email()
    password = settings.get_password()
    if email and password:
        helper.log('Logging in', 'Using stored credentials')
        try:
            token = api.get_token(email, password)
            settings.set_token(token)
        except api.LoginError as err:
            helper.log('Login with stored credentials failed', err, xbmc.LOGINFO)
        except Exception as err: # pylint: disable=broad-except
            helper.log('Login with stored credentials failed with unexpected err', err, xbmc.LOGERROR)
