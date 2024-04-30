import networkx as nx
import numpy as np
from pyvis.network import Network
import matplotlib.pyplot as plt
import pickle
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
import http.client
import re

from bs4 import BeautifulSoup

colors = ["b", "r", "g", "m", "y"]



def create_nodes_and_links_from_author(G, data, author):
    """
    Creates nodes and links in a graph based on the given author and co-authors data.

    Parameters:
    - G (networkx.Graph): The graph to add nodes and links to.
    - data (dict): The data containing information about the author and co-authors.
    - author (str): The name of the author.

    Returns:
    - G (networkx.Graph): The updated graph with added nodes and links.
    """
    G.add_node(author, label=author, group=1)

    for co_author in data["author"]["co_authors"]:
        G.add_node(co_author["name"], label=co_author["name"], group=1)
        G.add_edge(author, co_author["name"])
    return G


def one_level_graph(G, data, author):
    """
    Generate links between an given author and all its co_authors (one node only).

    Parameters:
    - G (networkx.Graph): The graph to add nodes and links to.
    - data (dict): The data containing information about authors and their connections.
    - author (str): The author to create the graph from.

    Returns:
    - G (networkx.Graph): The updated graph with nodes and links added.
    """
    G = create_nodes_and_links_from_author(G, data, author)
    return G


def draw(G):
    """
    Draw a graph using the Fruchterman-Reingold layout algorithm.

    Parameters:
    - G: NetworkX graph object

    Returns:
    None
    """
    pos = nx.fruchterman_reingold_layout(G, scale=2)
    nx.draw(G, pos)

    plt.show()
def saving_edge_list(G, filename):
    """
    Save the edge list of a graph to a file.

    Parameters:
    - G (networkx.Graph): The graph to save the edge list from.
    - filename (str): The name of the file to save the edge list to.

    Returns:
    None
    """
    nx.write_edgelist(G, filename, data=False, delimiter=";")

def create_coauthor_graph(path_to_edglist=None, depth_graphs=2, init_author = None):
    """
    Creates a co-author graph based on the provided edge list and the maximum number of nodes from initial author (depth_graphs).

    Args:
        path_to_edglist (str): The path to the edge list file.
        depth_graphs (int): The depth of the co-author graphs to create.

    Returns:
        None
    """
    ## Load the data
    with open(path_to_edglist, "rb") as handle:
        data = pickle.load(handle)   
    list_authors = list(data.keys())
    done_authors = [list_authors[0]]
    author = init_author if init_author is not None else list_authors[0]


    G = nx.Graph()
    G = one_level_graph(G, data[author], author)
    saving_edge_list(G, f"../profiles/graphs/{author} level {0}.csv")

    ## make the graph deeper -> coauthors of coauthors and so on.
    for level in range(depth_graphs):
        new_authors = list(G.nodes)
        for new_author in new_authors:
            if new_author not in done_authors:
                try:
                    G = one_level_graph(G, data[new_author], new_author)
                    done_authors += [new_author]
                except:
                    pass
        saving_edge_list(G, f"../profiles/graphs/{author} level {level+1}.csv")

