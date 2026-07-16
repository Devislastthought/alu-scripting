#!/usr/bin/python3
"""
Module to recursively query Reddit API for all hot posts.
"""

import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries Reddit API and returns a list of all hot article titles.
    
    Args:
        subreddit (str): The name of the subreddit (without the 'r/' prefix)
        hot_list (list): List to accumulate hot article titles (default: [])
        after (str): Pagination token for next page (default: None)
    
    Returns:
        list: List of all hot article titles, or None if subreddit is invalid
    """
    
    if not subreddit or not isinstance(subreddit, str):
        return None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {}
    if after:
        params['after'] = after
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=5
        )
        
        if response.status_code != 200:
            return None if not hot_list else hot_list
        
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        if not posts:
            return hot_list if hot_list else None
        
        # Add titles to the list
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)
        
        # Check if there are more pages
        after_token = data.get('data', {}).get('after')
        if after_token:
            return recurse(subreddit, hot_list, after_token)
        else:
            return hot_list if hot_list else None
    
    except Exception:
        return None if not hot_list else hot_list
