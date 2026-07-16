#!/usr/bin/python3
"""
Module to query Reddit API for subreddit subscriber counts.
"""

import requests


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit (without the 'r/' prefix)
    
    Returns:
        int: Total number of subscribers in the subreddit.
             Returns 0 if the subreddit is invalid or cannot be accessed.
    """
    
    if not subreddit or not isinstance(subreddit, str):
        return 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    
    try:
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            timeout=5
        )
        
        if response.status_code != 200:
            return 0
        
        data = response.json()
        subscribers = data.get('data', {}).get('subscribers', 0)
        
        return int(subscribers)
    
    except Exception:
        return 0
