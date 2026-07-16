#!/usr/bin/python3
"""
Module that recursively queries the Reddit API, parses the titles of
all hot articles for a subreddit, and prints a sorted count of given
keywords.
"""
import requests


def count_words(subreddit, word_list, instances=None, after=None):
    """
    Recursively queries the Reddit API, parses the titles of all hot
    articles for a given subreddit, and prints a sorted count of
    given keywords (case-insensitive).

    Args:
        subreddit (str): the name of the subreddit to search.
        word_list (list): the list of keywords to count.
        instances (dict): accumulator dict of word counts
            (used internally).
        after (str): pagination token (used internally).
    """
    if instances is None:
        instances = {}
        for word in word_list:
            key = word.lower()
            if key not in instances:
                instances[key] = 0

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu-student)"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params,
                             allow_redirects=False)

    if response.status_code != 200:
        return

    try:
        data = response.json().get("data", {})
    except ValueError:
        return

    posts = data.get("children", [])
    if not posts and after is None:
        return

    for post in posts:
        title = post.get("data", {}).get("title", "")
        for token in title.split():
            key = token.lower()
            if key in instances:
                instances[key] += 1

    next_after = data.get("after")
    if next_after is not None and posts:
        return count_words(subreddit, word_list, instances, next_after)

    if not any(instances.values()):
        return

    sorted_words = sorted(instances.items(), key=lambda item: (-item[1],
                                                                 item[0]))
    for word, count in sorted_words:
        if count > 0:
            print("{}: {}".format(word, count))
