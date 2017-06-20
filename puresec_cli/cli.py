#!/usr/bin/env python3

import sys

if sys.version_info.major != 3:
    print("Sorry, requires Python 3.x")
    sys.exit(1)

from argparse import ArgumentParser
from importlib import import_module
from puresec_cli import actions
from puresec_cli.stats import Stats

def main(argv=None):
    parser = ArgumentParser(
        description="Set of wonderful tools to improve your serverless security (and social life)."
    )

    parser.add_argument('--stats', choices=['enable', 'disable'],
                        help="Enable/disable sending anonymous statistics (on by default)")


    subparsers = parser.add_subparsers(title="Available commands")

    for action_name in actions.__all__:
        action = import_module("puresec_cli.actions.{}.action".format(action_name)).Action

        subparser = subparsers.add_parser(action.command(), **action.argument_parser_options())
        action.add_arguments(subparser)
        subparser.set_defaults(action=action)

    args = parser.parse_args()

    stats = Stats()
    stats.args = args

    ran = False

    if args.stats:
        ran = True
        stats.toggle(args.stats)

    if hasattr(args, 'action'):
        ran = True
        try:
            action = args.action(args, stats)
            action.run()
        except SystemExit:
            stats.result(action, 'Expected error')
            raise
        except Exception:
            stats.result(action, 'Unexpected error')
            raise
        else:
            stats.result(action, 'Successful run')

    if not ran:
        parser.print_usage()

if __name__ == '__main__':
    main()
