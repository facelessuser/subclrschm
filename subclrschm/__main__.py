"""Sublime Text Color Scheme Editor."""
from __future__ import unicode_literals
import os
import sys
from .lib.gui import custom_app
from .lib.gui import subclrschm_app
from .lib import parse_args
from .lib import util

# Handle case where pythonw.exe is used and there is not a valid stdout or stderr
if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")


def get_log_location():
    """Get log location."""

    platform = util.platform()

    if platform == "windows":
        folder = os.path.expanduser("~\\.subclrschm")
        fifo = os.path.join(folder, '\\\\.\\pipe\\subclrschm')
    elif platform == "osx":
        folder = os.path.expanduser("~/.subclrschm")
        fifo = os.path.join(folder, 'subclrschm.fifo')
    elif platform == "linux":
        folder = os.path.expanduser("~/.config/subclrschm")
        fifo = os.path.join(folder, 'subclrschm.fifo')

    if not os.path.exists(folder):
        os.mkdir(folder)

    return folder, fifo


def run():
    """Run the app."""

    args = parse_args.parse_arguments()
    def_loacation, fifo = get_log_location()

    if not args.log:
        args.log = def_loacation
    if os.path.exists(args.log):
        args.log = os.path.join(os.path.normpath(args.log), 'subclrschm.log')

    custom_app.init_app_log(args.log)
    if args.debug:
        custom_app.set_debug_mode(True)

    app = subclrschm_app.SubClrSchmApp(
        redirect=not args.no_redirect,
        single_instance_name="subclrschm" if not args.multi_instance else None,
        pipe_name=fifo if not args.multi_instance else None
    )

    if args.multi_instance or app.is_instance_okay():

        action = ""
        if args.select:
            action = "select"
        elif args.new:
            action = "new"

        main_win = subclrschm_app.Editor(
            None,
            live_save=args.live_save,
            debugging=args.debug
        )

        main_win.Show()
        main_win.init_frame(args.file, action)

        if main_win.is_ready():
            app.MainLoop()
    return 0


def main():
    """Main entry point."""

    sys.exit(run())


if __name__ == "__main__":
    main()
