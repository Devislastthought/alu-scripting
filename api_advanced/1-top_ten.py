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
    user_agent = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://www.reddit.com/r/{}/hot/.json?limit=10'.format(subreddit)
    try:
        response = requests.get(url, headers=user_agent,
                                 allow_redirects=False)
        if response.status_code != 200:
            print(None)
            return
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            print(None)
            return
        for post in posts:
            print(post['data']['title'])
    except requests.exceptions.RequestException:
        print(None)
    except ValueError:
        print(None)
