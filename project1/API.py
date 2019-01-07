import os
import requests

# Check for environment variable
if not os.getenv("GOODREADS_API_KEY"):
    raise RuntimeError("GOODREADS_API_KEY is not set")

#get api key
KEY = os.getenv("GOODREADS_API_KEY")

def get_average_gr_rating(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})
    if res.ok == True:
        return res.json()['books'][0]['average_rating']

    return None

