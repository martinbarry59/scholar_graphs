import sys
import os
from pathlib import Path

parent_dir = str(Path(os.getcwd()).parents[0])
sys.path.append(parent_dir + "/pkg/")
import scraping_utils as utils
import argparse


def main(args):
    """ scraping from initial author

    Parameters:
    args : argparse.Namespace
        The command-line arguments object, which holds all runtime specified parameters.
        - depth (int): Specifies the depth of the nodes from initial author to be generated. Optional, defaults to 2 if not specified.
        - name (str): Specifies the name of first assigned author. Optional, defaults to Martin Barry" if not specified.

    Examples:
    To run this function from the command line, use:
        python scrape_profiles.py --depth 3 --name "John Smith"

    If no arguments are provided, defaults are used:
        python scrape_profiles.py
    
    """
    name = args.name if args.name else "Martin Barry"
    depth = args.depth if args.depth else 2

    print("starting from profile of :", name)
    print("Depth of graphs:", depth)

    profiles = utils.scrape_coauthors_from_name(name, depth)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find all the co_authors of a given author up to a given depth."
    )
    parser.add_argument("--name", type=str, help="Name of first profile to scrape from")
    parser.add_argument(
        "--depth",
        type=int,
        help="number of nodes from initial author you want to scrape",
    )
    args = parser.parse_args()
    main(args)
