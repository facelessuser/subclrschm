"""Style settings panel."""
from __future__ import unicode_literals
import wx
from . import gui
from . import color_setting_dialog
from . import grid_helper
from . import settings_codes as sc
from ..rgba import RGBA
from ..x11colors import name2hex
from .. import util


class StyleSettings(gui.StyleSettingsPanel, grid_helper.GridHelper):
    """Style settings handler."""

    def __init__(self, parent, scheme, update):
        """Initialize."""

        super(StyleSettings, self).__init__(parent)
        if util.platform() == "windows":
            self.SetDoubleBuffered(False)
        self.diag = None
        self.setup_keybindings()
        self.parent = parent
        self.m_plist_grid.GetGridWindow().Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.m_plist_grid.SetDefaultCellBackgroundColour(self.GetBackgroundColour())
        self.read_plist(scheme)
        self.update_plist = update

    def read_plist(self, scheme):
        """Read the plist."""

        color = scheme["settings"][0]["settings"].get("foreground", "#000000").strip()
        if not color.startswith('#'):
            color = name2hex(color)
        foreground = RGBA(color)
        color = scheme["settings"][0]["settings"].get("background", "#FFFFFF").strip()
        if not color.startswith('#'):
            color = name2hex(color)
        background = RGBA(color)
        self.bg_color = background
        self.fg_color = foreground
        count = 0

        for s in scheme["settings"]:
            if "name" in s:
                self.m_plist_grid.AppendRows(1)
                self.update_row(count, s)
                count += 1
        self.resize_table()
        self.go_cell(self.m_plist_grid, 0, 0)

    def update_row(self, count, s):
        """Update stye row."""

        self.m_plist_grid.SetCellValue(count, 0, s["name"])
        self.m_plist_grid.SetCellValue(count, 4, s.get("scope", ""))
        settings = s["settings"]
        b = self.m_plist_grid.GetCellBackgroundColour(count, 0)
        if "background" in settings:
            try:
                named_color = name2hex(settings["background"].strip())
                color = named_color if named_color is not None else settings["background"].strip()
                bg = RGBA(color)
                bg.apply_alpha(self.bg_color.get_rgb())
                self.m_plist_grid.SetCellValue(count, 2, color)
            except:
                bg = self.bg_color
                self.m_plist_grid.SetCellValue(count, 2, "")
        else:
            bg = self.bg_color
        b = self.m_plist_grid.GetCellBackgroundColour(count, 0)
        b.Set(bg.r, bg.g, bg.b)
        self.m_plist_grid.SetCellBackgroundColour(count, 0, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 1, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 2, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 3, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 4, b)
        if "foreground" in settings:
            try:
                named_color = name2hex(settings["foreground"].strip())
                color = named_color if named_color is not None else settings["foreground"].strip()
                fg = RGBA(color)
                fg.apply_alpha(self.bg_color.get_rgb())
                self.m_plist_grid.SetCellValue(count, 1, color)
            except:
                fg = self.fg_color
                self.m_plist_grid.SetCellValue(count, 1, "")
        else:
            fg = self.fg_color
        f = self.m_plist_grid.GetCellTextColour(count, 0)
        f.Set(fg.r, fg.g, fg.b)
        self.m_plist_grid.SetCellTextColour(count, 0, f)
        self.m_plist_grid.SetCellTextColour(count, 1, f)
        self.m_plist_grid.SetCellTextColour(count, 2, f)
        self.m_plist_grid.SetCellTextColour(count, 3, f)
        self.m_plist_grid.SetCellTextColour(count, 4, f)

        fs_setting = settings.get("fontStyle", "")
        font_style = []
        for x in fs_setting.split(" "):
            if x in ["bold", "italic", "underline"]:
                font_style.append(x)

        self.m_plist_grid.SetCellValue(count, 3, " ".join(font_style))
        fs = self.m_plist_grid.GetCellFont(count, 0)
        fs.SetWeight(wx.FONTWEIGHT_NORMAL)
        fs.SetStyle(wx.FONTSTYLE_NORMAL)
        fs.SetUnderlined(False)

        if "bold" in font_style:
            fs.SetWeight(wx.FONTWEIGHT_BOLD)

        if "italic" in font_style:
            fs.SetStyle(wx.FONTSTYLE_ITALIC)

        if "underline" in font_style:
            fs.SetUnderlined(True)

        self.m_plist_grid.SetCellFont(count, 0, fs)
        self.m_plist_grid.SetCellFont(count, 1, fs)
        self.m_plist_grid.SetCellFont(count, 2, fs)
        self.m_plist_grid.SetCellFont(count, 3, fs)
        self.m_plist_grid.SetCellFont(count, 4, fs)

    def resize_table(self):
        """Resize the table."""

        self.m_plist_grid.BeginBatch()
        nb_size = self.parent.GetSize()
        total_size = 0
        for x in range(0, 5):
            self.m_plist_grid.AutoSizeColumn(x)
            total_size += self.m_plist_grid.GetColSize(x)
        delta = nb_size[0] - 20 - total_size
        if delta > 0:
            self.m_plist_grid.SetColSize(4, self.m_plist_grid.GetColSize(4) + delta)
        self.m_plist_grid.EndBatch()

    def set_object(self, obj):
        """Set the object."""

        row = self.m_plist_grid.GetGridCursorRow()
        self.update_row(row, obj)
        self.update_plist(sc.MODIFY, {"table": "style", "index": row, "data": obj})
        self.resize_table()

    def edit_cell(self):
        """Handle editting the cell."""

        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        editor = self.GetParent().GetParent().GetParent()
        self.diag = color_setting_dialog.ColorEditor(
            editor,
            {
                "name": grid.GetCellValue(row, 0),
                "scope": grid.GetCellValue(row, 4),
                "settings": {
                    "foreground": grid.GetCellValue(row, 1),
                    "background": grid.GetCellValue(row, 2),
                    "fontStyle": grid.GetCellValue(row, 3)
                }
            }
        )
        self.diag.ShowModal()
        self.diag.Destroy()
        self.diag = None

    def delete_row(self):
        """Handle row delete."""

        row = self.m_plist_grid.GetGridCursorRow()
        self.m_plist_grid.DeleteRows(row, 1)
        self.m_plist_grid.GetParent().update_plist(sc.DELETE, {"table": "style", "index": row})

    def insert_row(self):
        """Handle inserting into row."""

        obj = {
            "name": "New Item",
            "scope": "comment",
            "settings": {
                "foreground": "#FFFFFF",
                "background": "#000000",
                "fontStyle": ""
            }
        }
        editor = self.GetParent().GetParent().GetParent()
        self.diag = color_setting_dialog.ColorEditor(
            editor,
            obj,
            insert=True
        )
        self.diag.ShowModal()
        self.diag.Destroy()
        self.diag = None

    def row_up(self):
        """Handle row up."""

        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        if row > 0:
            text = [grid.GetCellValue(row, x) for x in range(0, 5)]
            bg = [grid.GetCellBackgroundColour(row, x) for x in range(0, 5)]
            fg = [grid.GetCellTextColour(row, x) for x in range(0, 5)]
            font = [grid.GetCellFont(row, x) for x in range(0, 5)]
            grid.DeleteRows(row, 1, False)
            grid.InsertRows(row - 1, 1, True)
            [grid.SetCellValue(row - 1, x, text[x]) for x in range(0, 5)]
            [grid.SetCellBackgroundColour(row - 1, x, bg[x]) for x in range(0, 5)]
            [grid.SetCellTextColour(row - 1, x, fg[x]) for x in range(0, 5)]
            [grid.SetCellFont(row - 1, x, font[x]) for x in range(0, 5)]
            self.go_cell(grid, row - 1, col, True)
            grid.GetParent().update_plist(sc.MOVE, {"from": row, "to": row - 1})
            grid.SetFocus()

    def row_down(self):
        """Handle row down."""

        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        if row < grid.GetNumberRows() - 1:
            text = [grid.GetCellValue(row, x) for x in range(0, 5)]
            bg = [grid.GetCellBackgroundColour(row, x) for x in range(0, 5)]
            fg = [grid.GetCellTextColour(row, x) for x in range(0, 5)]
            font = [grid.GetCellFont(row, x) for x in range(0, 5)]
            grid.DeleteRows(row, 1, False)
            grid.InsertRows(row + 1, 1, True)
            [grid.SetCellValue(row + 1, x, text[x]) for x in range(0, 5)]
            [grid.SetCellBackgroundColour(row + 1, x, bg[x]) for x in range(0, 5)]
            [grid.SetCellTextColour(row + 1, x, fg[x]) for x in range(0, 5)]
            [grid.SetCellFont(row + 1, x, font[x]) for x in range(0, 5)]
            self.go_cell(grid, row + 1, col, True)
            grid.GetParent().update_plist(sc.MOVE, {"from": row, "to": row + 1})
            grid.SetFocus()

    def is_fontstyle_cell(self):
        """Check if fontstyle cell."""

        return self.m_plist_grid.GetGridCursorCol() == 3

    def toggle_font_style(self, row, attr):
        """Toggle the font style."""

        # if not self.is_fontstyle_cell():
        #     return
        grid = self.m_plist_grid
        text = [grid.GetCellValue(row, x) for x in range(0, 5)]
        style = text[3].split(" ")
        try:
            idx = style.index(attr)
            del style[idx]
        except:
            style.append(attr)
        text[3] = " ".join(style)

        obj = {
            "name": text[0],
            "scope": text[4],
            "settings": {
                "foreground": text[1],
                "background": text[2],
                "fontStyle": text[3]
            }
        }
        grid.GetParent().update_row(row, obj)
        self.update_plist(sc.MODIFY, {"table": "style", "index": row, "data": obj})
        self.resize_table()

    def toggle_bold(self):
        """Toggle bold."""

        self.toggle_font_style(self.m_plist_grid.GetGridCursorRow(), "bold")

    def toggle_italic(self):
        """Toggle italic."""

        self.toggle_font_style(self.m_plist_grid.GetGridCursorRow(), "italic")

    def toggle_underline(self):
        """Toggle underline."""

        self.toggle_font_style(self.m_plist_grid.GetGridCursorRow(), "underline")

    def on_mouse_motion(self, event):
        """Handle mouse motion event."""

        self.mouse_motion(event)

    def on_edit_cell(self, event):
        """Handle editing cell event."""

        self.edit_cell()

    def on_grid_key_down(self, event):
        """Handle key down event on grid."""

        self.grid_key_down(event)

    def on_grid_select_cell(self, event):
        """Handle grid select event."""

        self.grid_select_cell(event)

    def on_row_up_click(self, event):
        """Handle row up click."""

        self.row_up()

    def on_row_down_click(self, event):
        """Handle row down click."""

        self.row_down()

    def on_row_add_click(self, event):
        """Handle row add click."""

        self.insert_row()

    def on_row_delete_click(self, event):
        """Handle row delete click."""

        self.delete_row()

    def on_grid_label_left_click(self, event):
        """Handle grid label left click."""

        return
