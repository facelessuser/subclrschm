"""Parse arguments."""
from __future__ import unicode_literals
import argparse
from . import util
from . import __meta__


def parse_arguments(args=None):
    """Parse the command arguments."""

    parser = argparse.ArgumentParser(
        prog='subclrschm',
        description='Sublime Color Scheme Editor - Edit Sublime Color Scheme'
    )
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-redirect', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--multi-instance', '-m', action='store_true', default=False, help="Allow multiple instances")
    parser.add_argument(
        '--log', '-l', nargs='?', default='',
        help="Absolute path to directory to store log file"
    )
    parser.add_argument('--live-save', '-L', action='store_true', default=False, help="Enable live save.")
    # Mutually exclusinve flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--select', '-s', action='store_true', default=False, help="Prompt for theme selection")
    group.add_argument('--new', '-n', action='store_true', default=False, help="Open prompting for new theme to create")
    # Positional
    parser.add_argument('file', nargs='?', default=None, help='Theme file')
    return parser.parse_args(util.to_unicode_argv()[1:] if args is None else args)
