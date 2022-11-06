#!/usr/bin/env python3
#
# Gives us a git-style main command that calls subcommands.
#
# Copyright 2022: Joe Block <jpb@unixorn.net>
# License: Apache 2.0


import os
import subprocess
import sys

from thelogrus.cli import find_subcommand


def hmd_usage():
    """
    They called hdm with no subcommands, or we couldn't find a subcommand
    """
    myName = os.path.basename(sys.argv[0])
    print(
        f"{myName} calls subcommands - try '{myName} create device --help' for example."
    )


def hmd_driver():
    """
    Process the command line arguments, find and run the appropriate
    subcommand.

    We want to be able to do git-style handoffs to subcommands where if we
    do `hdm blah foo bar` and the executable `hdm-blah-foo` exists, we'll call
    it with the argument bar.

    We deliberately don't do anything with the arguments other than hand
    them off to the hdm subcommand found.

    Subcommands are responsible for their own argument parsing.
    """
    try:
        (command, args) = find_subcommand(sys.argv)

        # If we can't construct a subcommand from sys.argv, it'll still be able
        # to find this driver script, and re-running ourself isn't useful.
        if os.path.basename(command) == sys.argv[0]:
            print("Could not find a subcommand for %s" % " ".join(sys.argv))
            sys.exit(13)
    except RuntimeError as e:
        print(str(e))
        hmd_usage()
        sys.exit(13)
    subprocess.check_call([command] + args)


if __name__ == "__main__":
    hmd_driver()
