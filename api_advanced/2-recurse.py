#!/usr/bin/python3
"""
Module that recursively queries the Reddit API and
returns a list of all hot post titles for a subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively collects titles of all hot posts.
    Returns None if subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "alvin-reddit-api-practice"
    }

    params = {
        "after": after
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    posts = data.get("children", [])

    for post in posts:
        hot_list.append(post.get("data", {}).get("title"))

    after = data.get("after")

    if after is None:
        return hot_list

    return recurse(subreddit, hot_list, after)