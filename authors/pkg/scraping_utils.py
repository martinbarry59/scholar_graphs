import networkx as nx
import numpy as np
from pyvis.network import Network
import matplotlib.pyplot as plt
import pickle
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
import http.client
import re
import time
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
from pathlib import Path

## Loading and making a global variable for all the known ids to avoid re-scraping the same author
parent_dir = str(Path(os.getcwd()).parents[0])
sys.path.append(parent_dir + "/pkg/")
known_ids = []
with open(parent_dir + "/profiles/all_people_datas.pickle", "rb") as handle:
    author_results_data = pickle.load(handle)
for key in author_results_data.keys():
    known_ids += [author_results_data[key]["author"]["id"]]


def find_author_by_id(author_id, author_results_data):
    """
    Find the author by their ID in the given author_results_data.

    Parameters:
    - author_id (str): The ID of the author to search for.
    - author_results_data (dict): A dictionary containing author results data.

    Returns:
    - str: The key of the author in the author_results_data dictionary if found, None otherwise.
    """
    for key in author_results_data.keys():
        if author_results_data[key]["author"]["id"] == author_id:
            return key


def find_coauthors_by_id(author_id):
    """
    Find co-authors of an author based on their ID.

    Parameters:
    author_id (str): The ID of the author.

    Returns:
    list: A list of co-authors of the author.

    """
    with open(parent_dir + "/profiles/all_people_datas.pickle", "rb") as handle:
        author_results_data = pickle.load(handle)

    author = find_author_by_id(author_id, author_results_data)
    print(author)
    return author_results_data[author]["author"]["co_authors"]

def scrape_scholar_from_id(author_id):
    print("extracting author results..")

    conn = http.client.HTTPSConnection("scholar.google.com")
    payload = ""
    headers = {
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "host": "scholar.google.com",
        "Cookie": "NID=513=A_TQidGwgoWn1r-_fIKMEK6qI8ZhsYYf3-cLbCR7lRKt1HVGMJ-5hGoZdQ82rwO4s0OjCTCuru9A750w_sX3hi4G-6mdgK_sbwtv7vhgCyW49naoH0jQDeB9Ei2cj48CFYWmS2p_G9BblPJIFV0SA0YrdfvOxTqo-ito88gKTME; GSP=LM=1713182346:S=YOPeDSx41ZX3GxTb",
    }
    conn.request("GET", f"/citations?user={author_id}&hl=en&oi=ao", payload, headers)
    res = conn.getresponse()

    data = res.read()
    soup = BeautifulSoup(data, "html.parser")
    return soup, res
def author_results(author_id, try_again=0):
    """
    Extracts author results from Google Scholar.

    Args:
        author_id (str): The ID of the author.
        try_again (int, optional): The number of times to retry the request if it fails. Defaults to 0.

    Returns:
        list: A list of dictionaries containing the author's name, ID, and co-authors.

    Raises:
        None: If the request fails and the maximum number of retries is reached.
    """
    pattern = r"user=([^&]+)"
    author_results_data = []
    soup, res = scrape_scholar_from_id(author_id)
    if res.status != 200:
        print(res.status)
        time.sleep(600)
        if try_again == 0:
            return author_results(author_id, try_again=1)
        else:
            return None
    author_name = soup.select("#gsc_prf_in")[0].text
    author_id = author_id
    print(f"Parsing {author_name}")
    co_authors = []

    for el in soup.select(".gsc_rsb_aa"):
        co_author = {}
        co_author["name"] = el.select(".gsc_rsb_a_desc a")[0].text
        match = re.search(pattern, str(el.select(".gsc_rsb_a_desc")[0]))
        co_author["id"] = match.group(1)
        co_authors += [co_author]
        print(co_author)

    author_results_data.append(
        {"name": author_name, "id": author_id, "co_authors": co_authors}
    )
    return author_results_data


def scrape_data_profile(author_id, root=4):
    """
    Scrapes data for a given author's profile.

    Args:
        author_id (str): The ID of the author.
        root (int, optional): The maximum depth of co-authors to scrape. Defaults to 4.

    Returns:
        None
    """
    global known_ids
    if not author_id in known_ids:
        known_ids += [author_id]
        author_results_data = author_results(author_id)

        if author_results_data is not None:
            results = {}
            results["author"] = author_results_data[0]
            coauthors = results["author"]["co_authors"]
            try:

                with open(
                    parent_dir + "/profiles/all_people_datas.pickle", "rb"
                ) as handle:
                    data = pickle.load(handle)
                    data[results["author"]["name"]] = results
                with open(
                    parent_dir + "/profiles/all_people_datas.pickle", "wb"
                ) as handle:
                    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            except:
                print("creating file for the first time")
                data = {}
                data[results["author"]["name"]] = results
                with open(
                    parent_dir + "/profiles/all_people_datas.pickle", "wb"
                ) as handle:
                    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif not root <= 0:
        print("already scraped")
        coauthors = find_coauthors_by_id(author_id)
    if not root <= 0 and coauthors is not None:
        for co_author in coauthors:
            scrape_data_profile(co_author["id"], root=root - 1)

def scrape_Scholar_from_name(name):
    """
    research name a scrap values from scholar.

    Args:
        name (str): The name of the author.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML data.

    """
    conn = http.client.HTTPSConnection("scholar.google.com")
    payload = ""
    headers = {
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "host": "scholar.google.com",
        "Cookie": "NID=513=A_TQidGwgoWn1r-_fIKMEK6qI8ZhsYYf3-cLbCR7lRKt1HVGMJ-5hGoZdQ82rwO4s0OjCTCuru9A750w_sX3hi4G-6mdgK_sbwtv7vhgCyW49naoH0jQDeB9Ei2cj48CFYWmS2p_G9BblPJIFV0SA0YrdfvOxTqo-ito88gKTME; GSP=LM=1713182346:S=YOPeDSx41ZX3GxTb",
    }
    conn.request(
        "GET",
        f"/citations?hl=en&view_op=search_authors&mauthors={name}&btnG=",
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()

    soup = BeautifulSoup(data, "html.parser")
    return soup
def scrape_coauthors_from_name(name, depth):
    """
    Scrapes coauthors from a given name using Google Scholar.

    Args:
        name (str): The name of the author to scrape coauthors for.
        depth (int): The depth of the scraping process.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the scraping process.
    """
    pattern = r'user=([^"]+)'
    name = name.replace(" ", "+")
    try:
        soup = scrape_Scholar_from_name(name)
        ## make a loop in case there exist multiple author with said name... (to perfect)
        for el in soup.select(".gs_ai_t"):
            match = re.search(pattern, str(el.select(".gs_ai_name")[0]))
            # If a match is found, extract the content between user= and "
            if match:
                author_id = match.group(1)
                print("name", name, " User ID:", author_id)
                scrape_data_profile(author_id, depth)

            else:
                print("No match found.")

    except Exception as e:
        print(e)
