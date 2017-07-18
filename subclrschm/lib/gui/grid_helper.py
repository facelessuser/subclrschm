"""Helper for gird objects."""
from __future__ import unicode_literals
import sys
import wx
from ..rgba import RGBA


class GridHelper(object):
    """Grid helper."""

    cell_select_semaphore = False
    range_semaphore = False
    current_row = None
    current_col = None

    def setup_keybindings(self):
        """Setup grid keybindings."""

        deleteid = wx.NewId()
        insertid = wx.NewId()

        self.Bind(wx.EVT_MENU, self.on_delete_row, id=deleteid)
        self.Bind(wx.EVT_MENU, self.on_insert_row, id=insertid)

        accel_tbl = wx.AcceleratorTable(
            [
                (wx.ACCEL_NORMAL, wx.WXK_DELETE, deleteid),
                (wx.ACCEL_CMD, ord('I'), insertid) if sys.platform == "darwin" else (wx.ACCEL_CTRL, ord('I'), insertid)
            ]
        )
        self.SetAcceleratorTable(accel_tbl)

    def go_cell(self, grid, row, col, focus=False):
        """Go to cell."""

        if focus:
            grid.GoToCell(row, col)
        else:
            grid.SetGridCursor(row, col)
        bg = grid.GetCellBackgroundColour(row, 0)
        lum = RGBA(bg.GetAsString(wx.C2S_HTML_SYNTAX)).get_luminance()
        if lum > 128:
            bg.Set(0, 0, 0)
        else:
            bg.Set(255, 255, 255)
        grid.SetCellHighlightColour(bg)

    def mouse_motion(self, event):
        """Capture if mouse is dragging."""

        if event.Dragging():       # mouse being dragged?
            pass                   # eat the event
        else:
            event.Skip()           # no dragging, pass on to the window

    def grid_key_down(self, event):
        """Check for certain key down events in the grid."""

        no_modifiers = event.GetModifiers() == 0
        alt_mod = event.GetModifiers() == wx.MOD_ALT
        if no_modifiers and event.GetKeyCode() == ord('B'):
            self.toggle_bold()
            return
        elif no_modifiers and event.GetKeyCode() == ord('I'):
            self.toggle_italic()
            return
        elif no_modifiers and event.GetKeyCode() == ord('U'):
            self.toggle_underline()
            return
        elif no_modifiers and event.GetKeyCode() == wx.WXK_RETURN:
            self.edit_cell()
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_UP:
            self.row_up()
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_DOWN:
            self.row_down()
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_LEFT:
            self.on_panel_left(event)
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_RIGHT:
            self.on_panel_right(event)
            return
        elif event.AltDown():
            # Eat...NOM NOM
            if event.GetKeyCode() == wx.WXK_UP:
                return
            elif event.GetKeyCode() == wx.WXK_DOWN:
                return
            elif event.GetKeyCode() == wx.WXK_LEFT:
                return
            elif event.GetKeyCode() == wx.WXK_RIGHT:
                return
        elif event.ShiftDown():
            # Eat...NOM NOM
            if event.GetKeyCode() == wx.WXK_UP:
                return
            elif event.GetKeyCode() == wx.WXK_DOWN:
                return
            elif event.GetKeyCode() == wx.WXK_LEFT:
                return
            elif event.GetKeyCode() == wx.WXK_RIGHT:
                return
        event.Skip()

    def grid_select_cell(self, event):
        """Grid cell selected."""

        grid = self.m_plist_grid
        if not self.cell_select_semaphore and event.Selecting():
            self.cell_select_semaphore = True
            self.current_row = event.GetRow()
            self.current_col = event.GetCol()
            self.go_cell(grid, self.current_row, self.current_col)
            self.cell_select_semaphore = False
        event.Skip()

    def on_panel_left(self, event):
        """Handle left key press."""

        grid = self.m_plist_grid
        grid.GetParent().GetParent().ChangeSelection(0)
        grid.GetParent().GetParent().GetPage(0).m_plist_grid.SetFocus()

    def on_panel_right(self, event):
        """Handle right key press."""

        grid = self.m_plist_grid
        grid.GetParent().GetParent().ChangeSelection(1)
        grid.GetParent().GetParent().GetPage(1).m_plist_grid.SetFocus()

    def on_row_up(self, event):
        """Handle row up."""

        self.row_up()

    def on_row_down(self, event):
        """Handle row down."""

        self.row_down()

    def on_insert_row(self, event):
        """Handle insert row."""

        self.insert_row()

    def on_delete_row(self, event):
        """Handle delete row."""

        self.delete_row()

    def on_edit_cell_key(self, event):
        """Handle edit cell key."""

        self.edit_cell()

    def on_toggle_bold(self, event):
        """Handle bold event."""

        self.toggle_bold()

    def on_toggle_italic(self, event):
        """Handle italic event."""

        self.toggle_italic()

    def on_toggle_underline(self, event):
        """Handle underline event."""

        self.toggle_underline()

    def toggle_bold(self):
        """Override for toggle bold."""

    def toggle_italic(self):
        """Override for toggle italic."""

    def toggle_underline(self):
        """Override for toggle underline."""

    def row_up(self):
        """Override row up."""

    def row_down(self):
        """Override for row down."""

    def edit_cell(self):
        """Override for edit cell."""

    def delete_row(self):
        """Override for delete row."""

    def insert_row(self):
        """Override for insert tow."""
