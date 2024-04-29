import sys
import os
from pathlib import Path

parent_dir = str(Path(os.getcwd()).parents[0])
sys.path.append(parent_dir + "/pkg/")
import graph_utils as utils
import argparse

def main(args):
    """ Creating the graph from connectivity matrix

    Parameters:
    args : argparse.Namespace
        The command-line arguments object, which holds all runtime specified parameters.
        - depth_graphs (int): Specifies the depth of the graphs to be generated. Optional, defaults to 2 if not specified.
        - path_to_edgelist (str): Specifies the path to the edge list data file. Optional, defaults to "profiles/all_people_datas.pickle" relative to the parent directory if not specified.

    Examples:
    To run this function from the command line, use:
        python script_name.py --depth_graphs 3 --path_to_edgelist "/path/to/your/edgelist.pickle"

    If no arguments are provided, defaults are used:
        python script_name.py
    
    """
    path_to_edgelist = (
        args.path
        if args.path
        else os.path.join(parent_dir, "profiles", "all_people_datas.pickle")
    )
    depth_graphs = args.depth if args.depth else 2

    print("Using edge list at:", path_to_edgelist)
    print("Depth of graphs:", depth_graphs)

    utils.create_coauthor_graph(path_to_edgelist, depth_graphs=depth_graphs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create coauthor graphs based on given parameters."
    )
    parser.add_argument("--depth", type=int, help="Depth of the graphs to be generated")
    parser.add_argument("--path", type=str, help="Path to the edge list data file")

    args = parser.parse_args()
    main(args)
