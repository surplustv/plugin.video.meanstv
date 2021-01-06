"""
Module with UI helpers
"""
from __future__ import absolute_import
from builtins import str
import xbmc
import xbmcgui

DIALOG_HEADING = 'Means.TV'
NOTIFICATION_LENGTH = 5000

def log(prefix, msg, level=xbmc.LOGDEBUG):
    '''
    Prints a debug message to Kodi log
    '''
    xbmc.log('[{0}] {1}:  {2}'.format(DIALOG_HEADING, str(prefix), str(msg)), level)


def show_error_notification(msg, title=''):
    '''
    Show an error notification with sound
    '''
    heading = DIALOG_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_ERROR, NOTIFICATION_LENGTH, True)
    log(title, msg, xbmc.LOGERROR)


def show_info_notification(msg, title=''):
    '''
    Show an in notification without sound
    '''
    heading = DIALOG_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_INFO, NOTIFICATION_LENGTH, False)
