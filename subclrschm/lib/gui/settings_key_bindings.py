"""Settings key bindings."""
from __future__ import unicode_literals
import wx


class SettingsKeyBindings(object):
    """Key binding for settings."""

    def setup_keybindings(self):
        """Setup the key bindings."""
        self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)

    def on_char_hook(self, event):
        """Evaluate keycode on char hook."""

        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        event.Skip()
