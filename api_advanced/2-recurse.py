#!/usr/bin/python3
"""
Module that recursively queries the Reddit API and returns a list of
titles of all hot articles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list containing
    the titles of all hot articles for a given subreddit.

    Args:
        subreddit (str): the name of the subreddit to search.
        hot_list (list): accumulator list of titles (used internally).
        after (str): pagination token (used internally).

    Returns:
        list: titles of all hot articles, or None if the subreddit
            is invalid or has no results.
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu-student)"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params,
                             allow_redirects=False)

    if response.status_code != 200:
        return None if not hot_list else hot_list

    try:
        data = response.json().get("data", {})
    except ValueError:
        return None if not hot_list else hot_list

    posts = data.get("children", [])

    if not posts and not hot_list:
        return None

    for post in posts:
        hot_list.append(post.get("data", {}).get("title"))

    next_after = data.get("after")
    if next_after is None:
        return hot_list

    return recurse(subreddit, hot_list, next_after)
