#!/usr/bin/python3
"""
This module contains the function top_ten.
"""
import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10
    hot posts for a given subreddit. Prints None if the subreddit
    is invalid.
    """
    url = 'https://www.reddit.com/r/{}/hot/.json?limit=10'.format(subreddit)
    headers = {'User-Agent': 'My User Agent 1.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        print(None)
        return
    data = response.json().get('data')
    if data is None:
        print(None)
        return
    posts = data.get('children', [])
    if not posts:
        print(None)
        return
    for post in posts:
        print(post['data']['title'])
