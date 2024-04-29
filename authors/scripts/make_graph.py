import sys
import os
from pathlib import Path
parent_dir = str(Path(os.getcwd()).parents[0])
sys.path.append(parent_dir+'/pkg/')
import graph_utils as utils
import argparse

def main(args):
    path_to_edgelist = args.path if args.path else os.path.join(parent_dir, 'profiles', 'all_people_datas.pickle')
    depth_graphs = args.depth if args.depth else 2

    print("Using edge list at:", path_to_edgelist)
    print("Depth of graphs:", depth_graphs)

    utils.create_coauthor_graph(path_to_edgelist, depth_graphs=depth_graphs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create coauthor graphs based on given parameters.")
    parser.add_argument('--depth', type=int, help='Depth of the graphs to be generated')
    parser.add_argument('--path', type=str, help='Path to the edge list data file')
    
    args = parser.parse_args()
    main(args)
