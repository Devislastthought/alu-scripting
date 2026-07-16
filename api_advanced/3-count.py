#!/usr/bin/python3
"""
Module to recursively query Reddit API and count keywords in hot post titles.
"""

import requests
import re


def count_words(subreddit, word_list, hot_list=[], after=None):
    """
    Recursively queries Reddit API, parses titles, and counts keywords.
    
    Args:
        subreddit (str): The name of the subreddit (without the 'r/' prefix)
        word_list (list): List of keywords to count (case-insensitive)
        hot_list (list): List to accumulate titles (for recursion)
        after (str): Pagination token for next page
    
    Returns:
        None: Prints sorted keyword counts to stdout
    """
    
    if not subreddit or not isinstance(subreddit, str):
        return
    
    if not word_list or not isinstance(word_list, list):
        return
    
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
            return
        
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        if not posts:
            if not hot_list:
                return
            else:
                _print_word_counts(hot_list, word_list)
                return
        
        # Add titles to the list
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)
        
        # Check if there are more pages
        after_token = data.get('data', {}).get('after')
        if after_token:
            return count_words(subreddit, word_list, hot_list, after_token)
        else:
            _print_word_counts(hot_list, word_list)
            return
    
    except Exception:
        return


def _print_word_counts(titles, word_list):
    """
    Counts keywords in titles and prints sorted results.
    
    Args:
        titles (list): List of post titles
        word_list (list): List of keywords to count
    """
    
    # Normalize word list to lowercase and count duplicates
    word_count_dict = {}
    for word in word_list:
        word_lower = word.lower()
        word_count_dict[word_lower] = word_count_dict.get(word_lower, 0)
    
    # Count occurrences in titles
    title_count_dict = {}
    for title in titles:
        # Split title into words
        words_in_title = re.findall(r'\b\w+\b', title.lower())
        for word in words_in_title:
            if word in word_count_dict:
                title_count_dict[word] = title_count_dict.get(word, 0) + 1
    
    # Sort by count (descending), then alphabetically (ascending)
    sorted_words = sorted(
        title_count_dict.items(),
        key=lambda x: (-x[1], x[0])
    )
    
    # Print results
    for word, count in sorted_words:
        print(f"{word}: {count}")
