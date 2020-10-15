"""
Module with UI helpers
"""

import xbmcgui

DIALOG_HEADING = 'Means.TV'
NOTIFICATION_LENGTH = 5000


def show_error_notification(msg, title=''):
    '''
    Show an error notification with sound
    '''
    heading = DIALOG_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_ERROR, NOTIFICATION_LENGTH, True)


def show_info_notification(msg, title=''):
    '''
    Show an in notification without sound
    '''
    heading = DIALOG_HEADING
    if title:
        heading += ': ' + str(title)
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, str(msg), xbmcgui.NOTIFICATION_INFO, NOTIFICATION_LENGTH, False)
