#!/usr/bin/env python3
"""
Module to query Reddit API for subreddit subscriber counts.
"""

import requests
import json


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit (without the 'r/' prefix)
    
    Returns:
        int: Total number of subscribers in the subreddit.
             Returns 0 if the subreddit is invalid or cannot be accessed.
    
    Note:
        - Requires requests library
        - Uses custom User-Agent to avoid rate limiting
        - Does NOT follow redirects (invalid subreddits redirect to search)
    
    Examples:
        >>> number_of_subscribers('python')
        1000000  # approximate
        
        >>> number_of_subscribers('nonexistent_subreddit_12345')
        0
    """
    
    if not subreddit or not isinstance(subreddit, str):
        return 0
    
    # Custom User-Agent header to avoid "Too Many Requests" errors
    headers = {
        'User-Agent': 'python-requests/2.28.0'
    }
    
    # Construct Reddit API URL
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    
    try:
        # GET request without following redirects
        # This is crucial because invalid subreddits redirect to search results
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            timeout=5
        )
        
        # Check for successful response
        if response.status_code != 200:
            return 0
        
        # Parse JSON and extract subscriber count
        data = response.json()
        subscribers = data.get('data', {}).get('subscribers', 0)
        
        return int(subscribers)
    
    except (requests.RequestException, ValueError, KeyError, TypeError):
        # Network errors, JSON parsing errors, or missing data
        return 0
    except Exception:
        # Catch all other exceptions
        return 0


if __name__ == "__main__":
    # Test with various subreddits
    test_subreddits = [
        'python',
        'learnprogramming',
        'programming',
        'Holberton',
        'SiliconValley',
        'nonexistent_subreddit_xyz',
        'invalid123456789'
    ]
    
    for sub in test_subreddits:
        count = number_of_subscribers(sub)
        print(f"r/{sub}: {count} subscribers")
