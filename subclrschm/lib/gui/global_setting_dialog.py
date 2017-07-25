"""Global editor dialog."""
from __future__ import unicode_literals
import wx
from . import basic_dialogs
from . import gui
from . import settings_key_bindings
from . import settings_codes as sc
from ..rgba import RGBA
from .. import util


class GlobalEditor(gui.GlobalSetting, settings_key_bindings.SettingsKeyBindings):
    """GlobalEditor."""

    def __init__(self, parent, current_entries, name, value, insert=False):
        """Initialize."""

        super(GlobalEditor, self).__init__(parent)

        if util.platform() == "windows":
            self.SetDoubleBuffered(True)

        self.setup_keybindings()
        self.Fit()
        size = self.GetSize()
        self.SetMinSize(size)
        self.obj_key = name
        self.obj_val = value
        self.color_save = ""
        self.apply_settings = False
        self.color_setting = False
        self.m_color_picker.Disable()
        self.entries = current_entries
        self.current_name = name
        self.valid = True
        self.insert = bool(insert)

        self.m_name_textbox.SetValue(self.obj_key)
        try:
            RGBA(self.obj_val)
            self.color_setting = True
            self.color_save = self.obj_val
            self.m_color_picker.Enable()
            self.m_color_radio.SetValue(True)
            self.m_value_textbox.SetValue(self.obj_val)
        except:
            self.m_text_radio.SetValue(True)
            self.m_text_textbox.SetValue(self.obj_val)

    def on_color_button_click(self, event):
        """Handle color button click event."""

        if not self.color_setting:
            event.Skip()
            return
        color = None
        data = wx.ColourData()
        data.SetChooseFull(True)

        alpha = None

        text = self.m_value_textbox.GetValue()
        rgb = RGBA(text)
        if len(text) == 9:
            alpha == text[7:9]

        # set the default color in the chooser
        data.SetColour(wx.Colour(rgb.r, rgb.g, rgb.b))

        # construct the chooser
        dlg = wx.ColourDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            # set the panel background color
            color = dlg.GetColourData().GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            self.m_value_textbox.SetValue(color if alpha is None else color + alpha)
        dlg.Destroy()
        event.Skip()

    def on_radio_click(self, event):
        """Handle radio event."""
        obj = event.GetEventObject()
        if obj is self.m_color_radio:
            self.m_text_textbox.Disable()
            self.m_value_textbox.Enable()
            self.m_color_picker.Enable()
            self.color_setting = True
            try:
                RGBA(self.m_value_textbox.GetValue())
                self.on_color_change(event)
            except:
                self.m_value_textbox.SetValue("#000000")
            return
        else:
            self.color_setting = False
            self.m_color_picker.Disable()
            self.m_value_textbox.Disable()
            self.m_color_picker.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.m_text_textbox.Enable()
            self.m_color_picker.Refresh()
        event.Skip()

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

    def on_color_change(self, event):
        """Handle color change event."""

        if not self.color_setting:
            event.Skip()
            return
        text = self.m_value_textbox.GetValue()
        try:
            cl = RGBA(text)
        except:
            event.Skip()
            return

        cl.apply_alpha(self.Parent.m_style_settings.bg_color.get_rgb())
        bg = wx.Colour(cl.r, cl.g, cl.b)
        self.m_color_picker.SetBackgroundColour(bg)
        self.m_color_picker.Refresh()

    def on_color_focus(self, event):
        """Handle color focus event."""

        if not self.color_setting:
            event.Skip()
            return
        if self.color_setting:
            self.color_save = self.m_value_textbox.GetValue()
        event.Skip()

    def on_color_blur(self, event):
        """Handle color blur event."""

        if not self.color_setting:
            event.Skip()
            return
        if self.color_setting:
            text = self.m_value_textbox.GetValue()
            try:
                RGBA(text)
            except:
                self.m_value_textbox.SetValue(self.color_save)
        event.Skip()

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

    def on_set_color_close(self, event):
        """Handle set color close event."""

        self.obj_key = self.m_name_textbox.GetValue()
        self.current_name = self.obj_key

        if self.apply_settings:
            self.obj_val = (
                self.m_value_textbox.GetValue() if self.m_color_radio.GetValue() else self.m_text_textbox.GetValue()
            )

            if self.insert:
                grid = self.Parent.m_global_settings.m_plist_grid
                num = grid.GetNumberRows()
                row = grid.GetGridCursorRow()
                if num > 0:
                    grid.InsertRows(row, 1, True)
                else:
                    grid.AppendRows(1)
                    row = 0
                grid.GetParent().update_row(row, self.obj_key, self.obj_val)
                grid.GetParent().go_cell(grid, row, 0)
                self.Parent.update_plist(sc.ADD, {"table": "global", "index": self.obj_key, "data": self.obj_val})
            else:
                self.Parent.set_global_object(self.obj_key, self.obj_val)

        event.Skip()
