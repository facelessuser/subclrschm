"""
Sublime Text Color Scheme Editor.

Licensed under MIT
Copyright (c) 2013 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import unicode_literals
import sys
import codecs
import os
import plistlib
import threading
import time
import uuid
import wx
import traceback

from .about_dialog import AboutDialog
from .custom_app import DebugFrameExtender, PipeApp
from .custom_app import debug, debug_struct, error
from . import custom_statusbar
from . import basic_dialogs
from . import gui
from . import global_settings_panel
from . import style_settings_panel
from . import data
from . import settings_codes as sc
from ..default_new_theme import theme as default_new_theme
from .. import util

DEBUG_CONSOLE = False

SHORTCUTS = {
    "osx": '''
===Applicatioon Shortcuts===
Find Next: \u2318 + F
Find Next: \u2318 + G
Find Prev: \u2318 + \u21e7 + G
Save: \u2318 + S
Save As: \u2318 + \u21e7 + S

===Table Shortcuts===
Edit Row: Enter
Move Row Up (Style Settings): \u2325 + \u2191
Move Row Down (Style Settings): \u2325 + \u2193
Switch to Global Settings: \u2325 + \u2190
Switch to Style Settings: \u2325 + \u2192
Delete Row: \u232B
Insert Row: \u2318 + I
Toggle 'bold' font: B
Toggle 'italic' font: I
Toggle 'underlined' font: U
''',

    "windows": '''
===Applicatioon Shortcuts===
Find Next: Control + F
Find Next: Control + G
Find Prev: Control + Shift + G
Save: Control + S
Save As: Control + Shift + S

===Table Shortcuts===
Edit Row: Enter
Move Row Up (Style Settings): Alt + \u2191
Move Row Down (Style Settings): Alt + \u2193
Switch to Global Settings: Alt + \u2190
Switch to Style Settings: Alt + \u2192
Delete Row: Delete
Insert Row: Control + I
Toggle 'bold' font: B
Toggle 'italic' font: I
Toggle 'underlined' font: U
''',

    "linux": '''
===Applicatioon Shortcuts===
Find Next: Control + F
Find Next: Control + G
Find Prev: Control + Shift + G
Save: Control + S
Save As: Control + Shift + S

===Table Shortcuts===
Edit Row: Enter
Move Row Up (Style Settings): Alt + \u2191
Move Row Down (Style Settings): Alt + \u2193
Switch to Global Settings: Alt + \u2190
Switch to Style Settings: Alt + \u2192
Delete Row: Delete
Insert Row: Control + I
Toggle 'bold' font: B
Toggle 'italic' font: I
Toggle 'underlined' font: U
'''
}


#################################################
# Helper Functions
#################################################
def query_user_for_file(parent, action):
    """Query the user for file to use."""

    file_path = None
    select_file = action == "select"
    new_file = action == "new"
    select = False
    done = False
    wildcard = "*.tmTheme"
    if not select_file and not new_file:
        select = basic_dialogs.yesno(
            "Create a new theme or select an existing one?", "Color Scheme Editor", yes="Select", no="New"
        )
    elif select_file:
        select = True
    while not done:
        if select:
            result = basic_dialogs.filepicker("Choose a theme file:", "", wildcard)
            if result is not None:
                debug(result)
                if not result.lower().endswith(".tmtheme"):
                    basic_dialogs.errormsg("File must be of type '.tmtheme'")
                    debug("Select: Bad extension: %s" % result)
                    continue
                file_path = result
                debug("Select: File selected: %s" % file_path)
            done = True
        else:
            result = basic_dialogs.filepicker("Theme file to save:", "", wildcard, True)
            if result is not None:
                if not result.lower().endswith(".tmtheme"):
                    basic_dialogs.errormsg("File must be of type '.tmtheme'")
                    debug("New: Bad extension: %s" % result)
                    continue
                try:
                    with codecs.open(result, "w", "utf-8") as f:
                        f.write((util.dump_plist(default_new_theme) + '\n'))
                    file_path = result
                    debug("New: File selected: %s" % file_path)
                except Exception:
                    error(traceback.format_exc())
                    basic_dialogs.errormsg('There was a problem writing the theme file!')
            done = True
    return file_path


def parse_file(file_path):
    """Parse the scheme file."""

    t_file = None
    color_scheme = None

    try:
        with open(file_path, "rb") as f:
            color_scheme = plistlib.readPlist(f)
    except Exception:
        error(traceback.format_exc())
        basic_dialogs.errormsg('Unexpected problem trying to parse file!')

    if color_scheme is not None:
        t_file = file_path

    return t_file, color_scheme


#################################################
# Live Update Manager
#################################################
class LiveUpdate(threading.Thread):
    """
    Live update of the file.

    This is mainly so Sublime can refersh the theme as you edit.
    """

    def __init__(self, func, queue):
        """Initialize."""

        self.func = func
        self.queue = queue
        self.last_queue_len = len(queue)
        self.abort = False
        self.last_update = 0.0
        self.done = False
        self.locked = False
        threading.Thread.__init__(self)

    def kill_thread(self):
        """Kill thread."""

        self.abort = True

    def lock_queue(self):
        """Lock the queue."""

        if not self.is_queue_locked():
            self.locked = True
            return True
        return False

    def release_queue(self):
        """Release the queue."""

        if self.is_queue_locked():
            self.locked = False
            return True
        return False

    def is_queue_locked(self):
        """Check if queue is locked."""

        return self.locked

    def is_done(self):
        """Check if done."""

        return self.done

    def update(self, queue):
        """Update the theme."""

        wx.CallAfter(self.func, "Live Thread")

    def _process_queue(self):
        """Process the queue."""

        while not self.lock_queue():
            time.sleep(.2)
        current_queue = self.queue[0:self.last_queue_len]
        del self.queue[0:self.last_queue_len]
        self.last_queue_len = len(self.queue)
        self.release_queue()
        return current_queue

    def run(self):
        """Run the thread."""

        while not self.abort:
            now = time.time()
            if len(self.queue) and (now - .5) > self.last_update:
                if len(self.queue) != self.last_queue_len:
                    self.last_queue_len = len(self.queue)
                else:
                    self.update(self._process_queue())
                    self.last_update = time.time()
            if self.abort:
                break
            time.sleep(.5)
        if len(self.queue):
            self.update(self._process_queue())
        self.done = True


#################################################
# Editor Dialog
#################################################
class Editor(gui.EditorFrame, DebugFrameExtender):
    """Main editor."""

    def __init__(self, parent, live_save, debugging=False):
        """Initialize."""

        super(Editor, self).__init__(parent)
        self.ready = False
        self.opening = False
        self.m_global_settings = None
        self.m_style_settings = None
        if util.platform() == "windows":
            self.SetDoubleBuffered(True)
        self.SetIcon(data.get_image('subclrschm_large.png').GetIcon())
        self.live_save = bool(live_save)
        self.updates_made = False
        mod = wx.ACCEL_CMD if sys.platform == "darwin" else wx.ACCEL_CTRL
        self.set_keybindings(
            [
                (mod, ord('B'), self.on_shortcuts),
                (mod | wx.ACCEL_SHIFT, ord('S'), self.on_save_as),
                (mod, ord('S'), self.on_save),
                (mod, ord('F'), self.focus_find),
                (mod, ord('G'), self.on_next_find),
                (mod | wx.ACCEL_SHIFT, ord('G'), self.on_prev_find)
            ],
            self.on_debug_console if debugging else None
        )
        self.search_results = []
        self.cur_search = None
        self.last_UUID = None
        self.last_plist_name = None
        self.m_menuitem_save.Enable(False)
        self.queue = []
        self.debugging = debugging
        custom_statusbar.extend_sb(self.m_statusbar)
        self.m_main_panel.Fit()
        self.Fit()
        self.SetMinSize(self.GetSize())

    def init_frame(self, scheme_file, action):
        """Show the main frame."""

        t_file = None
        scheme = None

        if scheme_file is None:
            scheme_file = query_user_for_file(self, action)

        if scheme_file is not None:
            t_file, scheme = parse_file(scheme_file)

        if t_file is None:
            self.Close()
            return

        if self.debugging:
            self.open_debug_console()
        self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
        self.scheme = scheme
        self.tmtheme = t_file
        debug_struct(scheme, "Color Scheme")

        try:
            self.m_style_settings = style_settings_panel.StyleSettings(
                self.m_plist_notebook, scheme,
                self.update_plist
            )
            self.m_global_settings = global_settings_panel.GlobalSettings(
                self.m_plist_notebook, scheme,
                self.update_plist, self.rebuild_tables
            )
        except Exception as e:
            debug("Failed to load scheme settings!")
            debug(e)
            raise

        self.m_plist_name_textbox.SetValue(scheme["name"])
        self.m_plist_uuid_textbox.SetValue(scheme.get("uuid", ''))
        self.last_UUID = scheme.get("uuid", '')
        self.last_plist_name = scheme["name"]

        self.m_plist_notebook.InsertPage(0, self.m_global_settings, "Global Settings", True)
        self.m_plist_notebook.InsertPage(1, self.m_style_settings, "Scope Settings", False)
        if self.live_save:
            self.update_thread = LiveUpdate(self.save, self.queue)
            self.update_thread.start()

        self.ready = True

    def is_ready(self):
        """Get whether dialog is ready to show."""

        return self.ready

    def update_plist(self, code, args={}):
        """Update plist."""

        if code == sc.UUID:
            this_uuid = self.m_plist_uuid_textbox.GetValue()
            if this_uuid == "":
                if "uuid" in self.scheme:
                    del self.scheme["uuid"]
            else:
                self.scheme["uuid"] = self.m_plist_uuid_textbox.GetValue()
            self.updates_made = True
        elif code == sc.NAME:
            self.scheme["name"] = self.m_plist_name_textbox.GetValue()
            self.updates_made = True
        elif code == sc.ADD and args is not None:
            debug("Add")
            if args["table"] == "style":
                self.scheme["settings"].insert(args["index"] + 1, args["data"])
            else:
                self.scheme["settings"][0]["settings"][args["index"]] = args["data"]
            self.updates_made = True
        elif code == sc.DELETE and args is not None:
            debug("Delete")
            if args["table"] == "style":
                del self.scheme["settings"][args["index"] + 1]
            else:
                del self.scheme["settings"][0]["settings"][args["index"]]
            self.updates_made = True
        elif code == sc.MOVE and args is not None:
            debug("Move")
            from_row = args["from"] + 1
            to_row = args["to"] + 1
            item = self.scheme["settings"][from_row]
            del self.scheme["settings"][from_row]
            self.scheme["settings"].insert(to_row, item)
            self.updates_made = True
        elif code == sc.MODIFY and args is not None:
            debug("Modify")
            if args["table"] == "style":
                obj = {
                    "name": args["data"]["name"],
                    "scope": args["data"]["scope"],
                    "settings": {
                    }
                }

                settings = args["data"]["settings"]

                if settings["foreground"] != "":
                    obj["settings"]["foreground"] = settings["foreground"]

                if settings["background"] != "":
                    obj["settings"]["background"] = settings["background"]

                if settings["fontStyle"] != "":
                    obj["settings"]["fontStyle"] = settings["fontStyle"]

                self.scheme["settings"][args["index"] + 1] = obj
            else:
                self.scheme["settings"][0]["settings"][args["index"]] = args["data"]
            self.updates_made = True
        else:
            debug("No valid edit actions!")

        if self.live_save:
            while not self.update_thread.lock_queue():
                time.sleep(.2)
            self.queue.append("tmtheme")
            self.update_thread.release_queue()
        elif self.updates_made:
            self.m_statusbar.set_icon(
                "unsaved",
                data.get_bitmap('floppy.png'),
                msg="Unsaved changes"
            )
            self.m_menuitem_save.Enable(True)

    def rebuild_plist(self):
        """Rebuild plist."""

        self.scheme["name"] = self.m_plist_name_textbox.GetValue()
        this_uuid = self.m_plist_uuid_textbox.GetValue()
        if this_uuid == "":
            if "uuid" in self.scheme:
                del self.scheme['uuid']
        else:
            self.scheme["uuid"] = this_uuid
        self.scheme["settings"] = [{"settings": {}}]
        for r in range(0, self.m_global_settings.m_plist_grid.GetNumberRows()):
            key = self.m_global_settings.m_plist_grid.GetCellValue(r, 0)
            val = self.m_global_settings.m_plist_grid.GetCellValue(r, 1)
            self.scheme["settings"][0]["settings"][key] = val

        for r in range(0, self.m_style_settings.m_plist_grid.GetNumberRows()):
            name = self.m_style_settings.m_plist_grid.GetCellValue(r, 0)
            foreground = self.m_style_settings.m_plist_grid.GetCellValue(r, 1)
            background = self.m_style_settings.m_plist_grid.GetCellValue(r, 2)
            fontstyle = self.m_style_settings.m_plist_grid.GetCellValue(r, 3)
            scope = self.m_style_settings.m_plist_grid.GetCellValue(r, 4)

            obj = {
                "name": name,
                "scope": scope,
                "settings": {
                }
            }

            if foreground != "":
                obj["settings"]["foreground"] = foreground

            if background != "":
                obj["settings"]["background"] = background

            if fontstyle != "":
                obj["settings"]["fontStyle"] = fontstyle

            self.scheme["settings"].append(obj)

        if self.live_save:
            while not self.update_thread.lock_queue():
                time.sleep(.2)
            self.queue.append("tmtheme")
            self.update_thread.release_queue()

    def save(self, requester="Main Thread"):
        """Save."""

        debug("%s requested save" % requester)
        try:
            with codecs.open(self.tmtheme, "w", "utf-8") as f:
                f.write((util.dump_plist(self.scheme) + '\n'))
            self.updates_made = False
            if not self.live_save:
                self.m_statusbar.remove_icon('unsaved')
                self.m_menuitem_save.Enable(False)
        except Exception:
            error(traceback.format_exc())
            basic_dialogs.errormsg('Unexpected problem trying to write .tmTheme file!')

    def rebuild_tables(self, cur_row, cur_col):
        """Rebuild the tables."""

        cur_page = self.m_plist_notebook.GetSelection()

        self.m_global_settings.m_plist_grid.DeleteRows(0, self.m_global_settings.m_plist_grid.GetNumberRows())
        self.m_global_settings.read_plist(self.scheme)
        self.m_global_settings.go_cell(self.m_global_settings.m_plist_grid, 0, 0)

        self.m_style_settings.m_plist_grid.DeleteRows(0, self.m_style_settings.m_plist_grid.GetNumberRows())
        self.m_style_settings.read_plist(self.scheme)
        self.m_style_settings.go_cell(self.m_style_settings.m_plist_grid, 0, 0)

        if cur_page == 0:
            self.m_plist_notebook.ChangeSelection(cur_page)
            if cur_row is not None and cur_col is not None:
                self.m_global_settings.go_cell(self.m_global_settings.m_plist_grid, cur_row, cur_col, True)
        elif cur_page == 1:
            self.m_plist_notebook.ChangeSelection(cur_page)
            if cur_row is not None and cur_col is not None:
                self.m_style_settings.go_cell(self.m_style_settings.m_plist_grid, cur_row, cur_col, True)

    def set_style_object(self, obj):
        """Set style object."""

        self.m_style_settings.set_object(obj)

    def set_global_object(self, key, value):
        """Set global object."""

        self.m_global_settings.set_object(key, value)

    def focus_find(self, event):
        """Set focus on search panel."""

        self.m_search_panel.SetFocus()
        event.Skip()

    def find(self):
        """Find."""

        self.search_results = []
        pattern = self.m_search_panel.GetValue().lower()
        panel = self.m_style_settings if self.m_plist_notebook.GetSelection() else self.m_global_settings
        self.cur_search = panel
        grid = panel.m_plist_grid
        for r in range(0, grid.GetNumberRows()):
            for c in range(0, grid.GetNumberCols()):
                if pattern in grid.GetCellValue(r, c).lower():
                    self.search_results.append((r, c))

    def find_next(self, current=False):
        """Find next."""

        panel = self.m_style_settings if self.m_plist_notebook.GetSelection() else self.m_global_settings
        if self.cur_search is not panel:
            debug("Find: Panel switched.  Upate results.")
            self.find()
        grid = panel.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        next = None
        for i in self.search_results:
            if current and row == i[0] and col == i[1]:
                next = i
                break
            elif row == i[0] and col < i[1]:
                next = i
                break
            elif row < i[0]:
                next = i
                break
        if next is None and len(self.search_results):
            next = self.search_results[0]
        if next is not None:
            grid.SetFocus()
            panel.go_cell(grid, next[0], next[1], True)

    def find_prev(self, current=False):
        """Find previous."""

        panel = self.m_style_settings if self.m_plist_notebook.GetSelection() else self.m_global_settings
        if self.cur_search is not panel:
            debug("Find: Panel switched.  Upate results.")
            self.find()
        grid = panel.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        prev = None
        for i in reversed(self.search_results):
            if current and row == i[0] and col == i[1]:
                prev = i
                break
            elif row == i[0] and col > i[1]:
                prev = i
                break
            elif row > i[0]:
                prev = i
                break
        if prev is None and len(self.search_results):
            prev = self.search_results[-1]
        if prev is not None:
            grid.SetFocus()
            panel.go_cell(grid, prev[0], prev[1], True)

    def file_close_cleanup(self):
        """File close cleanup."""

        if self.live_save:
            self.update_thread.kill_thread()
            if self.live_save:
                while not self.update_thread.is_done():
                    time.sleep(0.5)
        elif not self.live_save and self.updates_made:
            if basic_dialogs.yesno(
                "You have unsaved changes.  Do you want to Save?",
                "Color Scheme Editor",
                yes="Save",
                no="Discard"
            ):
                self.save()
            else:
                self.updates_made = False
                self.m_statusbar.remove_icon('unsaved')
                self.m_menuitem_save.Enable(False)

    def check_name(self):
        """Check the name."""

        set_name = self.m_plist_name_textbox.GetValue()
        if set_name != self.last_plist_name:
            self.last_plist_name = set_name
            self.update_plist(sc.NAME)

    def check_uuid(self, event):
        """Check UUID."""

        try:
            set_uuid = self.m_plist_uuid_textbox.GetValue()
            if set_uuid == '':
                if set_uuid != self.last_UUID:
                    self.last_UUID = set_uuid
                    self.update_plist(sc.UUID)
            else:
                uuid.UUID(set_uuid)
                if set_uuid != self.last_UUID:
                    self.last_UUID = set_uuid
                    self.update_plist(sc.UUID)
        except Exception:
            self.on_uuid_button_click(event)
            error(traceback.format_exc())
            basic_dialogs.errormsg('UUID is invalid! A new UUID has been generated.')
            debug("Bad UUID: %s!" % self.m_plist_uuid_textbox.GetValue())

    def on_plist_name_blur(self, event):
        """Handle plist name blur event."""

        event.Skip()
        if not self.is_ready():
            return
        self.check_name()

    def on_name_enter(self, event):
        """Handle plist name on enter key."""

        event.Skip()
        self.check_name()

    def on_uuid_button_click(self, event):
        """Handle UUID button event."""

        self.last_UUID = str(uuid.uuid4()).upper()
        self.m_plist_uuid_textbox.SetValue(self.last_UUID)
        self.update_plist(sc.UUID)
        event.Skip()

    def on_uuid_blur(self, event):
        """Handle UUID blur event."""

        event.Skip()
        if not self.is_ready():
            return
        self.check_uuid(event)

    def on_uuid_enter(self, event):
        """Handle UUID on enter key."""

        event.Skip()
        self.check_uuid(event)

    def on_plist_notebook_size(self, event):
        """Handle plist notebook size event."""

        if self.m_global_settings and self.m_style_settings:
            self.m_global_settings.resize_table()
            self.m_style_settings.resize_table()
        event.Skip()

    def on_create_new(self, event):
        """Create new theme file."""

        self.opening = True

        scheme_file = query_user_for_file(self, action="new")

        if scheme_file:
            try:
                with codecs.open(scheme_file, "w", "utf-8") as f:
                    f.write((util.dump_plist(default_new_theme) + '\n'))
                file_path = scheme_file
                debug("New: File selected: %s" % file_path)
            except Exception:
                file_path = None
                error(traceback.format_exc())
                basic_dialogs.errormsg('There was a problem writing the theme file!')

            if file_path:
                self.open_new(file_path)
        self.opening = False

    def on_open_new(self, event):
        """Handle open new event."""

        self.opening = True
        scheme_file = query_user_for_file(self, action="select")
        self.open_new(scheme_file)
        self.opening = False

    def open_new(self, scheme_file):
        """Open new scheme file."""

        if scheme_file is not None:
            self.file_close_cleanup()
            t_file, color_scheme = parse_file(scheme_file)
            if t_file is not None:
                self.tmtheme = t_file
                self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
                self.scheme = color_scheme
                self.m_plist_name_textbox.SetValue(self.scheme["name"])
                self.m_plist_uuid_textbox.SetValue(self.scheme.get("uuid", ""))
                self.last_UUID = self.scheme.get("uuid", "")
                self.last_plist_name = self.scheme["name"]
                self.rebuild_tables(None, None)
                self.m_style_settings.resize_table()
                self.m_global_settings.resize_table()
                if self.live_save:
                    self.queue = []
                    self.update_thread = LiveUpdate(self.save, self.queue)
                    self.update_thread.start()

    def on_save(self, event):
        """Handle save event."""

        if not self.live_save:
            self.save()

    def on_save_as(self, event):
        """Handle save as event."""

        self.opening = True
        save_file = query_user_for_file(self, action="new")
        if save_file is not None:
            t_file = None
            t_file = save_file
            self.tmtheme = t_file
            self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
            if self.live_save:
                while not self.update_thread.lock_queue():
                    time.sleep(.2)
                del self.queue[0:len(self.queue)]
                self.update_thread.release_queue()
            self.save()
        self.opening = False

    def on_about(self, event):
        """Handle about event."""

        dlg = AboutDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def on_find(self, event):
        """Handle find event."""

        self.find()
        event.Skip()

    def on_find_finish(self, event):
        """Handle find finish event."""

        self.find_next(current=True)

    def on_next_find(self, event):
        """Handle next find event."""

        self.find_next()

    def on_prev_find(self, event):
        """Handle previous find event."""

        self.find_prev()

    def on_shortcuts(self, event):
        """Handle shortcuts event."""

        if sys.platform == "darwin":
            msg = SHORTCUTS["osx"]
        elif sys.platform == "linux2":
            msg = SHORTCUTS["linux"]
        else:
            msg = SHORTCUTS["windows"]
        basic_dialogs.infomsg(msg, "Shortcuts")

    def on_debug_console(self, event):
        """Handle debug console event."""

        self.open_debug_console()

    def on_close(self, event):
        """Handle close event."""

        self.close_debug_console()
        self.file_close_cleanup()
        event.Skip()


class SubClrSchmApp(PipeApp):
    """SubClrSchmApp."""

    def __init__(self, *args, **kwargs):
        """Init SubClrSchmApp object."""

        PipeApp.__init__(self, *args, **kwargs)

    def on_pipe_args(self, event):
        """
        Handle piped arguments.

        When receiving arguments via named pipes,
        look for the search path argument, and populate
        the search path in the RummageFrame
        """

        from .. import parse_args
        from .platform_window_focus import platform_window_focus

        if event.data:
            # Prevent further clicks and such

            args = parse_args.parse_arguments(event.data)
            frame = self.GetTopWindow()
            if frame is not None:

                frame.Disable()
                if frame.opening or not frame.is_ready():
                    frame.Enable()
                    return

                # Close edit dialogs
                if frame.m_global_settings and frame.m_global_settings.diag:
                    frame.m_global_settings.diag.Close()
                if frame.m_style_settings and frame.m_style_settings.diag:
                    frame.m_style_settings.diag.Close()

                scheme_file = None
                if args.file:
                    scheme_file = args.file
                elif args.select:
                    platform_window_focus(frame)
                    scheme_file = frame.on_open_new(None)
                elif args.new:
                    platform_window_focus(frame)
                    scheme_file = frame.on_create_new(None)

                if scheme_file:
                    # Wait until saves are empty or we timeout
                    start = time.time()
                    while frame.queue:
                        if (time.time() - start) > 1.0:
                            break
                    # Open
                    frame.Enable()
                    frame.open_new(scheme_file)
                    platform_window_focus(frame)
                else:
                    frame.Enable()

    def process_args(self, arguments):
        """Event for processing the arguments."""
        from .. import parse_args

        argv = parse_args.parse_arguments(arguments)
        args = []

        if argv.select:
            args.append('-s')
        if argv.new:
            args.append('-n')
        if argv.file and os.path.exists(argv.file):
            args.append(os.path.abspath(argv.file))

        return args

    def MacReopenApp(self):  # noqa
        """Ensure that app will be unminimized in OSX on dock icon click."""

        from .platform_window_focus import platform_window_focus

        frame = self.GetTopWindow()
        platform_window_focus(frame)
