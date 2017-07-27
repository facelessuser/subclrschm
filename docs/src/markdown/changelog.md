# Changelog

## 2.3.0

Jul 26, 2017

- **NEW**: Add menu entry to create a new color scheme.
- **NEW**: Show visual indicator when unsaved changes are present.
- **NEW**: Apply name and UUID if enter is pressed in the respective text box.
- **NEW**: `phantomCss` and `popupCss` are no longer treated special but like an ordinary text entry. Text entries have a separate box that can optionally contain multi-line data or single line data.
- **NEW**: Slight redesign of edit dialogs.
- **NEW**: When in single instance mode, pipe arguments to existing instance.
- **NEW**: Minor tweaks to GUI.
- **FIX**: Ensure a new live thread is started when switching files.
- **FIX**: Fix issue where event isn't passed into UUID check.
- **FIX**: When opening new file while another file is open, don't clean up current file until after the new file has been selected and successfully parsed.

## 2.0.2

Jul 23, 2017

- **FIX**: `UUID` should be optional.

## 2.0.1

Jul 23, 2017

- **FIX**: Include images as data in `setup.py` when installing.

## 2.0.0

Jul 23, 2017

- **NEW**: Add support for X11 color names.  Convert them to hex on color scheme load.
- **NEW**: Handle `popupCss` and `phantomCss`. Inject them if they are missing.
- **NEW**: Require `wxPython` 4+ and rework code to use it and support Python 2.7 and 3.4+.
- **NEW**: Remove importing and exporting of JSON color schemes.
- **FIX**: Multiple Ubuntu dock icons (possibly similar issue in other Linux distros).

## 1.0.0

- **NEW**: Initial release.
