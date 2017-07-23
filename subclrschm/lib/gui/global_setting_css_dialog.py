"""Global editor dialog."""
from __future__ import unicode_literals
from . import basic_dialogs
from . import gui
from . import settings_key_bindings
from .. import util


class GlobalCssEditor(gui.GlobalSettingCss, settings_key_bindings.SettingsKeyBindings):
    """GlobalCssEditor."""

    def __init__(self, parent, current_entries, name, value, insert=False):
        """Initialize."""

        super(GlobalCssEditor, self).__init__(parent)
        if util.platform() == "windows":
            self.SetDoubleBuffered(True)
        self.setup_keybindings()
        self.Fit()
        size = self.GetSize()
        self.SetMinSize(size)
        size.Set(-1, size[1])
        self.obj_key = name
        self.obj_val = value
        self.apply_settings = False
        self.entries = current_entries
        self.current_name = name
        self.valid = True

        self.m_name_textbox.SetValue(self.obj_key)
        self.m_value_textbox.WriteText(self.obj_val)

    def is_name_valid(self):
        """Check if name is valid."""

        valid = True
        name = self.m_name_textbox.GetValue()
        if name != self.current_name:
            for k in self.entries:
                if name == k:
                    valid = False
                    break
        return valid

    def on_global_name_blur(self, event):
        """Handle global name blur event."""

        if not self.is_name_valid():
            basic_dialogs.errormsg(
                "Key name \"%s\" already exists in global settings. "
                "Please use a different name." % self.m_name_textbox.GetValue()
            )
            self.m_name_textbox.SetValue(self.current_name)
        else:
            self.current_name = self.m_name_textbox.GetValue()

    def on_apply_button_click(self, event):
        """Handle apply button click event."""

        self.m_apply_button.SetFocus()
        if self.is_name_valid():
            self.apply_settings = True
            self.Close()
        else:
            basic_dialogs.errormsg(
                "Key name \"%s\" already exists in global settings. "
                "Please use a different name." % self.m_name_textbox.GetValue()
            )
            self.m_name_textbox.SetValue(self.current_name)

    def on_close(self, event):
        """Handle set color close event."""

        self.obj_key = self.m_name_textbox.GetValue()
        self.current_name = self.obj_key

        if self.apply_settings:
            self.obj_val = self.m_value_textbox.GetValue()
            self.Parent.set_global_object(self.obj_key, self.obj_val)

        event.Skip()
