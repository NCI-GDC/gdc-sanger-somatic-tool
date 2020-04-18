"""
Main entrypoint for all gdc-sanger-tools. 
"""
import argparse
import datetime
import sys

from signal import signal, SIGPIPE, SIG_DFL

from gdc_sanger_tools.logger import Logger
from gdc_sanger_tools.subcommands import CheckBamHeader 


signal(SIGPIPE, SIG_DFL)

def main(args=None, extra_subparser=None):
    """
    The main method for gdc-sanger-tools. 
    """
    # Setup logger
    Logger.setup_root_logger()

    logger = Logger.get_logger("main")

    # Get args
    p = argparse.ArgumentParser("GDC Sanger Tools")
    subparsers = p.add_subparsers(dest="subcommand")
    subparsers.required = True

    CheckBamHeader.add(subparsers=subparsers)

    if extra_subparser:
        extra_subparser.add(subparsers=subparsers)

    options = p.parse_args(args)

    # Run
    options.func(options)

    # Finish
    logger.info("Finished!")

if __name__ == '__main__':
    main()
