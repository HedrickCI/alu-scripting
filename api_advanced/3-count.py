#!/usr/bin/python3
"""
Module that recursively queries the Reddit API,
counts given keywords in hot post titles,
and prints them sorted by frequency.
"""

import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively count keyword occurrences in hot posts.
    """

    if counts is None:
        counts = {}

        # Normalize word_list and initialize counts
        for word in word_list:
            word_lower = word.lower()
            counts[word_lower] = counts.get(word_lower, 0)

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
        return None if after is None else None

    data = response.json().get("data", {})
    posts = data.get("children", [])

    for post in posts:
        title = post.get("data", {}).get("title", "")
        words = title.lower().split()

        for word in words:
            if word in counts:
                counts[word] += 1

    after = data.get("after")

    if after is not None:
        return count_words(subreddit, word_list, after, counts)

    # Final call — print sorted results
    sorted_counts = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    for word, count in sorted_counts:
        if count > 0:
            print("{}: {}".format(word, count))

    return