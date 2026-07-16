#!/usr/bin/env python3
"""
Query Reddit API to get the number of subscribers for a subreddit.
"""

import requests
import json


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of subscribers for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit (without the r/ prefix)
    
    Returns:
        int: The number of subscribers. Returns 0 if the subreddit is invalid.
    
    Note:
        - Invalid subreddits may return a redirect to search results
        - No following redirects to avoid counting search results as valid
        - Sets a custom User-Agent to avoid "Too Many Requests" errors
    """
    
    # Custom User-Agent to avoid rate limiting
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'
    }
    
    # Construct the API URL
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    
    try:
        # Make request WITHOUT following redirects
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)
        
        # If not a 200 status code, the subreddit is invalid
        if response.status_code != 200:
            return 0
        
        # Parse JSON response
        data = response.json()
        
        # Extract subscriber count from the data
        subscribers = data['data']['subscribers']
        
        return subscribers
    
    except (requests.RequestException, ValueError, KeyError):
        # Return 0 for any errors (invalid subreddit, network error, JSON parse error, etc.)
        return 0


if __name__ == "__main__":
    # Test cases
    print(f"r/programming subscribers: {number_of_subscribers('programming')}")
    print(f"r/learnprogramming subscribers: {number_of_subscribers('learnprogramming')}")
    print(f"r/invalid_subreddit_xyz subscribers: {number_of_subscribers('invalid_subreddit_xyz')}")
    print(f"r/python subscribers: {number_of_subscribers('python')}")
