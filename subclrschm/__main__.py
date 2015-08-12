"""Sublime Text Color Scheme Editor."""
from __future__ import unicode_literals
import argparse
import os
import sys
from .subclrschm import version
from .subclrschm.gui import custom_app
from .subclrschm.gui import subclrschm_app

PY3 = (3, 0) <= sys.version_info < (4, 0)
CLI_ENCODING = sys.getfilesystemencoding()

if PY3:
    binary_type = bytes  # noqa
else:
    binary_type = str  # noqa


def pyin(value):
    """Read in stdin variables."""

    return value.decode(CLI_ENCODING) if isinstance(value, binary_type) else value


def parse_arguments(script):
    """Parse the command arguments."""

    parser = argparse.ArgumentParser(
        prog='subclrschm',
        description='Sublime Color Scheme Editor - Edit Sublime Color Scheme'
    )
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + version.__version__))
    parser.add_argument('--debug', '-d', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument(
        '--log', '-l', nargs='?', default=script, type=pyin,
        help="Absolute path to directory to store log file"
    )
    parser.add_argument('--live_save', '-L', action='store_true', default=False, help="Enable live save.")
    # Mutually exclusinve flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--select', '-s', action='store_true', default=False, help="Prompt for theme selection")
    group.add_argument('--new', '-n', action='store_true', default=False, help="Open prompting for new theme to create")
    # Positional
    parser.add_argument('file', nargs='?', default=None, type=pyin, help='Theme file')
    return parser.parse_args()


def run():
    """Run the app."""

    cs = None
    j_file = None
    t_file = None
    script = os.path.dirname(os.path.abspath(sys.argv[0]))
    args = parse_arguments(script)

    if os.path.exists(args.log):
        args.log = os.path.join(os.path.normpath(args.log), 'subclrschm.log')

    custom_app.init_app_log(args.log)
    if args.debug:
        custom_app.set_debug_mode(True)
    custom_app.debug('Starting ColorSchemeEditor')
    custom_app.debug('Arguments = %s' % str(args))

    app = custom_app.CustomApp(redirect=args.debug)  # , single_instance_name="subclrschm")
    if args.file is None:
        action = ""
        if args.select:
            action = "select"
        elif args.new:
            action = "new"
        args.file = subclrschm_app.query_user_for_file(None, action)

    if args.file is not None:
        j_file, t_file, cs = subclrschm_app.parse_file(args.file)

    if j_file is not None and t_file is not None:
        main_win = subclrschm_app.Editor(
            None, cs, j_file, t_file,
            live_save=args.live_save, debugging=args.debug
        )
        main_win.Show()
        app.MainLoop()
    return 0


def main():
    """Main entry point."""

    sys.exit(run())


if __name__ == "__main__":
    main()
