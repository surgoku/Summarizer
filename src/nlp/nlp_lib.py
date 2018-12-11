import wikipedia
from urllib.request import urlopen
import re
import json

from nltk.tokenize import sent_tokenize
from newsapi import NewsApiClient

import sys
import time
sys.path.insert(0, './nlp/')
sys.path.insert(0, '../src/')

from config import *

newsapi = NewsApiClient(api_key='d4e78f4dadf04ca0bbffffee00748259')


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def tokenize_article_to_sentences(article):
    return sent_tokenize(article)


def get_wiki_article(input_str):
    #try:
    wiki = wikipedia.summary(input_str)
    return  wiki

'''
def get_news_article(input_str):
    api_key = 'd4e78f4dadf04ca0bbffffee00748259'
    api_url = 'https://newsapi.org/v2/everything?q=' + '%20'.join(input_str.split()) + '&from=2018-10-11&sortBy=publishedAt&apiKey=' + api_key
    jsonurl = urlopen(api_url)
    text = json.loads(jsonurl.read())

    news_list = []

    if 'articles' in text:
        articles = text['articles']
        for article in articles:
            if 'content' in article:
                news_list.append(article['content'])

    news_list = [i for i in news_list if i]

    return " ".join(news_list[:50])
'''

def get_news_article(input_str):
    text = newsapi.get_everything(q=input_str)
    #time.sleep(1)
    news_list = []
    if 'articles' in text:
        articles = text['articles']
        for article in articles:
            if 'content' in article:
                news_list.append(article['content'])

    news_list = [i for i in news_list if i]

    return " ".join(news_list[:50])

def get_comments_from_reddit_post(reddit_streamer, post_id):
    submission_comments = reddit_streamer.submission(id=post_id)
    #time.sleep(0.25)
    comments = []
    for top_level_comment in submission_comments.comments:
        try:
            body = top_level_comment.body
            if body[0] == '[' or body[-1] == ']' or 'Edit:' in body:
                continue
            else:
                comments.append(striphtml(body))
        except:
            continue
    return comments


def get_reddit_comments_for_query(reddit_streamer, search):
    sortsub = "top"
    startNum = 0
    comment_list = []

    for submission in reddit_streamer.subreddit('all').search(search.lower(), sort=sortsub):
        startNum += 1
        title = submission.title
        post_id = submission.id
        comments = get_comments_from_reddit_post(reddit_streamer, post_id)
        if len(comments):
            comment_list.extend(comments)
        if len(comment_list) > 50:
            break

    comment_list = comment_list[:50]
    return " ".join(comment_list)

def get_articles(topic, reddit_streamer):
    article_sources = [get_wiki_article, get_reddit_comments_for_query, get_news_article]
    source_names = ['wiki:fact', 'reddit:opinion', "news"]

    source_article_map = {}
    is_none = False
    try:
        for Source, name in zip(article_sources, source_names):
            if 'reddit' in name:
                source_article_map[name] = Source(reddit_streamer, topic)
            else:
                source_article_map[name] = Source(topic)
        return source_article_map
    except:
        return None





if __name__ == '__main__':

    query = 'narendra modi'
    query = 'sjsu'

    #print (get_news_article(query))

    #print (get_wiki_head(query))

    #reddit_streamer = get_reddit_streamer()
    #print (get_reddit_comments_for_query(reddit_streamer, query))