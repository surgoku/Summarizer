import sys
sys.path.insert(0, './nlp/')
sys.path.insert(0, '../src/')

import praw
from config import *

def get_reddit_streamer():
    reddit_streamer = praw.Reddit(client_id=clientid,
                         client_secret=clientsecret,
                         password=password,
                         user_agent='Reddit search data extractor by /u/' + username + '',
                        username=username)

    return  reddit_streamer