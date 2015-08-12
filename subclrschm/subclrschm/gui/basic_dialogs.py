"""Basic dialogs."""
from __future__ import unicode_literals
from . import messages
from .custom_app import error


def filepicker(msg, wildcard, save=False):
    """Call file picker."""

    return messages.filepickermsg(msg, wildcard, save)


def yesno(question, title='Yes or no?', bitmap=None, yes="Okay", no="Cancel"):
    """Prompt for yes/no."""

    return messages.promptmsg(question, title, bitmap, yes, no)


def infomsg(msg, title="INFO", bitmap=None):
    """Info message."""

    messages.infomsg(msg, title, bitmap)


def errormsg(msg, title="ERROR", bitmap=None):
    """Error message."""

    error(msg)
    messages.errormsg(msg, title, bitmap)


def warnmsg(msg, title="WARNING", bitmap=None):
    """Warning message."""

    messages.warnmsg(msg, title, bitmap)
