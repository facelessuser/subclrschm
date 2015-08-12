"""
Sublime Text Color Scheme Editor.

Licensed under MIT
Copyright (c) 2013 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import unicode_literals
import sys
import codecs
import json
import os
import plistlib
import threading
import time
import uuid
import wx
from wx.lib.embeddedimage import PyEmbeddedImage

from . import basic_dialogs
from . import gui
from . import global_settings_panel
from . import style_settings_panel
from . import settings_codes as sc
from .custom_app import DebugFrameExtender
from .custom_app import debug, debug_struct
from ..default_new_theme import theme as default_new_theme
from ..file_strip.json import sanitize_json
from .. import version

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


# Icon by Isaac Muse
AppIcon = PyEmbeddedImage(
    "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")


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
    if sys.platform == "darwin":
        wildcard = "(*.tmTheme;*.tmTheme.JSON)|*.tmTheme;*.JSON"
    else:
        wildcard = "(*.tmTheme;*.tmTheme.JSON)|*.tmTheme;*.tmTheme.JSON"
    if not select_file and not new_file:
        select = basic_dialogs.yesno(
            "Create a new theme or select an existing one?", "Color Scheme Editor", yes="Select", no="New"
        )
    elif select_file:
        select = True
    while not done:
        if select:
            result = basic_dialogs.filepicker("Choose a theme file:", wildcard)
            if result is not None:
                debug(result)
                if not result.lower().endswith(".tmtheme.json") and not result.lower().endswith(".tmtheme"):
                    basic_dialogs.errormsg("File must be of type '.tmtheme' or '.tmtheme.json'")
                    debug("Select: Bad extension: %s" % result)
                    continue
                file_path = result
                debug("Select: File selected: %s" % file_path)
            done = True
        else:
            result = basic_dialogs.filepicker("Theme file to save:", wildcard, True)
            if result is not None:
                if not result.lower().endswith(".tmtheme.json") and not result.lower().endswith(".tmtheme"):
                    basic_dialogs.errormsg("File must be of type '.tmtheme' or '.tmtheme.json'")
                    debug("New: Bad extension: %s" % result)
                    continue
                if result.lower().endswith("tmtheme.json"):
                    with codecs.open(result, "w", "utf-8") as f:
                        f.write(
                            (
                                json.dumps(
                                    default_new_theme,
                                    sort_keys=True, indent=4, separators=(',', ': ')
                                ) + '\n'
                            ).decode('raw_unicode_escape')
                        )
                else:
                    with codecs.open(result, "w", "utf-8") as f:
                        f.write((plistlib.writePlistToString(default_new_theme) + '\n').decode('utf8'))
                file_path = result
                debug("New: File selected: %s" % file_path)
            done = True
    return file_path


def parse_file(file_path):
    """Parse the scheme file."""

    j_file = None
    t_file = None
    color_scheme = None
    is_json = file_path.lower().endswith("tmtheme.json")

    try:
        with open(file_path, "r") as f:
            color_scheme = json.loads(sanitize_json(f.read(), True)) if is_json else plistlib.readPlist(f)
    except Exception:
        basic_dialogs.errormsg('Unexpected problem trying to parse file!')

    if color_scheme is not None:
        if is_json:
            j_file = file_path
            t_file = file_path[:-5]

            if not os.path.exists(t_file):
                try:
                    with codecs.open(t_file, "w", "utf-8") as f:
                        f.write((plistlib.writePlistToString(color_scheme) + '\n').decode('utf8'))
                except Exception:
                    debug("tmTheme file write error!")
        else:
            j_file = file_path + ".JSON"
            t_file = file_path

            if not os.path.exists(j_file):
                try:
                    with codecs.open(j_file, "w", "utf-8") as f:
                        f.write(
                            (
                                json.dumps(
                                    color_scheme,
                                    sort_keys=True, indent=4, separators=(',', ': ')
                                ) + '\n'
                            ).decode('raw_unicode_escape')
                        )
                except Exception:
                    debug("JSON file write error!")

    return j_file, t_file, color_scheme


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

        request = None
        for x in queue:
            if x == "all":
                request = x
                break
            elif x == "json":
                if request == "tmtheme":
                    request = "all"
                else:
                    request = x
            elif x == "tmtheme":
                if request == "json":
                    request = "all"
                    break
                else:
                    request = x

        wx.CallAfter(self.func, request, "Live Thread")

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

    def __init__(self, parent, scheme, j_file, t_file, live_save, debugging=False):
        """Initialize."""

        super(Editor, self).__init__(parent)
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
        if debugging:
            self.open_debug_console()
        self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
        self.search_results = []
        self.cur_search = None
        self.last_UUID = None
        self.last_plist_name = None
        self.scheme = scheme
        self.json = j_file
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
        self.m_plist_uuid_textbox.SetValue(scheme["uuid"])
        self.last_UUID = scheme["uuid"]
        self.last_plist_name = scheme["name"]

        self.m_menuitem_save.Enable(False)

        self.m_plist_notebook.InsertPage(0, self.m_global_settings, "Global Settings", True)
        self.m_plist_notebook.InsertPage(1, self.m_style_settings, "Scope Settings", False)
        self.queue = []
        if self.live_save:
            self.update_thread = LiveUpdate(self.save, self.queue)
            self.update_thread.start()

    def update_plist(self, code, args={}):
        """Update plist."""

        if code == sc.JSON_UUID:
            self.scheme["uuid"] = self.m_plist_uuid_textbox.GetValue()
            self.updates_made = True
        elif code == sc.JSON_NAME:
            self.scheme["name"] = self.m_plist_name_textbox.GetValue()
            self.updates_made = True
        elif code == sc.JSON_ADD and args is not None:
            debug("JSON add")
            if args["table"] == "style":
                self.scheme["settings"].insert(args["index"] + 1, args["data"])
            else:
                self.scheme["settings"][0]["settings"][args["index"]] = args["data"]
            self.updates_made = True
        elif code == sc.JSON_DELETE and args is not None:
            debug("JSON delete")
            if args["table"] == "style":
                del self.scheme["settings"][args["index"] + 1]
            else:
                del self.scheme["settings"][0]["settings"][args["index"]]
            self.updates_made = True
        elif code == sc.JSON_MOVE and args is not None:
            debug("JSON move")
            from_row = args["from"] + 1
            to_row = args["to"] + 1
            item = self.scheme["settings"][from_row]
            del self.scheme["settings"][from_row]
            self.scheme["settings"].insert(to_row, item)
            self.updates_made = True
        elif code == sc.JSON_MODIFY and args is not None:
            debug("JSON modify")
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
            self.m_menuitem_save.Enable(True)

    def rebuild_plist(self):
        """Rebuild plist."""

        self.scheme["name"] = self.m_plist_name_textbox.GetValue()
        self.scheme["uuid"] = self.m_plist_uuid_textbox.GetValue()
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

    def save(self, request, requester="Main Thread"):
        """Save."""

        debug("%s requested save - %s" % (requester, request))
        if request == "tmtheme" or request == "all":
            try:
                with codecs.open(self.tmtheme, "w", "utf-8") as f:
                    f.write((plistlib.writePlistToString(self.scheme) + '\n').decode('utf8'))
            except Exception:
                basic_dialogs.errormsg('Unexpected problem trying to write .tmTheme file!')

        if request == "json" or request == "all":
            try:
                with codecs.open(self.json, "w", "utf-8") as f:
                    f.write(
                        (
                            json.dumps(
                                self.scheme,
                                sort_keys=True, indent=4, separators=(',', ': ')
                            ) + '\n'
                        ).decode('raw_unicode_escape')
                    )
                self.updates_made = False
                if not self.live_save:
                    self.m_menuitem_save.Enable(False)
            except Exception:
                basic_dialogs.errormsg('Unexpected problem trying to write .tmTheme.JSON file!')

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
        if self.live_save and self.updates_made:
            self.save("json")
        elif not self.live_save and self.updates_made:
            if basic_dialogs.yesno("You have unsaved changes.  Save?", "Color Scheme Editor"):
                self.save("all")

    def on_plist_name_blur(self, event):
        """Handle plist name blur event."""

        set_name = self.m_plist_name_textbox.GetValue()
        if set_name != self.last_plist_name:
            self.last_plist_name = set_name
            self.update_plist(sc.JSON_NAME)
        event.Skip()

    def on_uuid_button_click(self, event):
        """Handle UUID button event."""

        self.last_UUID = str(uuid.uuid4()).upper()
        self.m_plist_uuid_textbox.SetValue(self.last_UUID)
        self.update_plist(sc.JSON_UUID)
        event.Skip()

    def on_uuid_blur(self, event):
        """Handle UUID blur event."""

        try:
            set_uuid = self.m_plist_uuid_textbox.GetValue()
            uuid.UUID(set_uuid)
            if set_uuid != self.last_UUID:
                self.last_UUID = set_uuid
                self.update_plist(sc.JSON_UUID)
        except Exception:
            self.on_uuid_button_click(event)
            basic_dialogs.errormsg('UUID is invalid! A new UUID has been generated.')
            debug("Bad UUID: %s!" % self.m_plist_uuid_textbox.GetValue())
        event.Skip()

    def on_plist_notebook_size(self, event):
        """Handle plist notebook size event."""

        self.m_global_settings.resize_table()
        self.m_style_settings.resize_table()
        event.Skip()

    def on_open_new(self, event):
        """Handle open new event."""

        self.file_close_cleanup()
        save_file = query_user_for_file(self, action="select")
        if save_file is not None:
            j_file, t_file, color_scheme = parse_file(save_file)
            if j_file is not None and t_file is not None:
                self.json = j_file
                self.tmtheme = t_file
                self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
                self.scheme = color_scheme
                self.m_plist_name_textbox.SetValue(self.scheme["name"])
                self.m_plist_uuid_textbox.SetValue(self.scheme["uuid"])
                self.last_UUID = self.scheme["uuid"]
                self.last_plist_name = self.scheme["name"]
                self.rebuild_tables(None, None)

    def on_save(self, event):
        """Handle save event."""

        if not self.live_save:
            self.save("all")

    def on_save_as(self, event):
        """Handle save as event."""

        save_file = query_user_for_file(self, action="new")
        if save_file is not None:
            j_file = None
            t_file = None
            is_json = save_file.lower().endswith("tmtheme.json")
            if is_json:
                j_file = save_file
                t_file = save_file[:-5]
            else:
                j_file = save_file + ".JSON"
                t_file = save_file
            self.json = j_file
            self.tmtheme = t_file
            self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
            if self.live_save:
                while not self.update_thread.lock_queue():
                    time.sleep(.2)
                del self.queue[0:len(self.queue)]
                self.update_thread.release_queue()
            self.save("all")

    def on_about(self, event):
        """Handle about event."""

        basic_dialogs.infomsg(
            "Color Scheme Editor: version %s" % version.__version__,
            bitmap=basic_dialogs.messages.MessageIcon(AppIcon.GetBitmap(), 64, 64)
        )
        event.Skip()

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
