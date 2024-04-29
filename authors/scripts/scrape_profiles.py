import sys
import os
from pathlib import Path
parent_dir = str(Path(os.getcwd()).parents[0])
sys.path.append(parent_dir+'/pkg/')
import scraping_utils as utils
import argparse

def main(args):
    name = args.name if args.name else 'Martin Barry'
    depth = args.depth if args.depth else 2

    print("starting from profile of :", name)
    print("Depth of graphs:", depth)

    profiles = utils.getScholarID(name, depth)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find all the co_authors of a given author up to a given depth.")
    parser.add_argument('--name', type=str, help='Name of first profile to scrape from')
    parser.add_argument('--depth', type=int, help='number of nodes from initial author you want to scrape')
    args = parser.parse_args()
    main(args)
