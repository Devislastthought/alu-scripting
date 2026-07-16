#!/usr/bin/python3
"""
Module to query Reddit API for top 10 hot posts.
"""

import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit (without the 'r/' prefix)
    
    Returns:
        None
    """
    
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    try:
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            timeout=5
        )
        
        if response.status_code != 200:
            print("None")
            return
        
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        if not posts:
            print("None")
            return
        
        for i, post in enumerate(posts[:10]):
            title = post.get('data', {}).get('title')
            if title:
                print(title)
    
    except Exception:
        print("None")
