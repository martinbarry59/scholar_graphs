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


def create_nodes_and_links(G, n_nodes, n_topics):
    nodes = {}
    for author in range(n_nodes):
        topic = topics[np.random.randint(n_topics)]
        nodes[author] = {"topic": topic, "edges": [], "color": colors[topic]}
        G.add_node(author, color=colors[topic])
        for reverse in range(G.nodes):
            chance = 0.9 if nodes[author]["topic"] == nodes[reverse]["topic"] else 0.0
            if chance > np.random.rand():
                nodes[author]["edges"] += [reverse]
                nodes[reverse]["edges"] += [author]
    return G, nodes


def create_list_authors(n_nodes, n_topics):
    topics = np.arange(topics_number)

    list_authors = {}
    for author in range(n_nodes):
        topic = topics[np.random.randint(n_topics)]
        list_authors[author] = {"topic": topic, "edges": [], "color": colors[topic]}
    return list_authors


def create_nodes_and_links_from_author(G, data, author):
    G.add_node(author, label=author, group=1)

    for co_author in data["author"]["co_authors"]:
        G.add_node(co_author["name"], label=co_author["name"], group=1)
        G.add_edge(author, co_author["name"])
    return G


def create_edges(G, data, nodes):
    for author in range(len(nodes)):
        for co_author in nodes[author]["edges"]:
            G.add_edge(author, co_author, color=colors[nodes[author]["topic"]])
    return G


def one_level_graph(G, data, author):
    G = create_nodes_and_links_from_author(G, data, author)

    return G


def draw(G):

    pos = nx.fruchterman_reingold_layout(G, scale=2)
    edges = G.edges()
    nx.draw(G, pos)

    plt.show()


def create_coauthor_graph(path_to_edglist=None, depth_graphs=2):
    with open(path_to_edglist, "rb") as handle:
        data = pickle.load(handle)
    G = nx.Graph()
    list_authors = list(data.keys())
    done_authors = [list_authors[0]]
    author = list_authors[0]
    G = one_level_graph(G, data[author], author)
    nx.write_edgelist(
        G, f"../profiles/graphs/{author} level {0}.csv", data=False, delimiter=";"
    )
    for level in range(depth_graphs):
        new_authors = list(G.nodes)
        for new_author in new_authors:
            if new_author not in done_authors:
                try:
                    G = one_level_graph(G, data[new_author], new_author)

                    done_authors += [new_author]
                except:
                    pass
        nx.write_edgelist(
            G,
            f"../profiles/graphs/{author} level {level+1}.csv",
            data=False,
            delimiter=";",
        )
