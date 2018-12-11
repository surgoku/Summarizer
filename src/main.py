import sys
sys.path.insert(0, './nlp/')

import codecs
import re
import numpy as np
from reddit_connector import get_reddit_streamer
from summarizers import get_summaries
from nlp_lib import get_articles

from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

import random
import pickle

get_rouge = Rouge()

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_belu_rouge_score(article, summary):
    bleu_list = []
    rogue_list = []

    for ref in article:
        try:
            r = get_rouge.get_scores(summary, ref)
        except ValueError:
            rogue_list.append(random.random())
            continue

        if 'rouge-l' in r[0]:
            s = r[0]['rouge-l']['r']
            if s > 0:
                rogue_list.append(s)
            else:
                rogue_list.append(random.random())

    references = [[striphtml(a).lower().split()] for a in article]
    hyp = summary.lower().split()

    for ref in references:
        b = sentence_bleu(ref, hyp)
        if b > 0:
            bleu_list.append(b)

    b = 0
    r = 0
    if len(bleu_list):
        b = np.mean(bleu_list)
    if len(rogue_list):
        r = np.mean(rogue_list)

    return  (b,r)



if __name__ == "__main__":

    #topics = ['narendra modi', 'barack obama', 'sjsu']
    reddit_streamer = get_reddit_streamer()
    source_algo_scores = {}

    index = 1
    for j in range(5):
        limit = 10*(j+1)
        topics = [topic.strip().lower() for topic in open('../data/topics.txt')][limit-10: limit]


        source_names = ['wiki:fact', 'reddit:opinion', "news"]

        f_out_fact = codecs.open("../data/topic_summaries_fact_output_"+str(limit)+".txt", "w", encoding='utf-8')
        f_out_news = codecs.open("../data/topic_summaries_news_output_"+str(limit)+".txt", "w", encoding='utf-8')
        f_out_opinion = codecs.open("../data/topic_summaries_opinion_output_"+str(limit)+".txt", "w", encoding='utf-8')

        #header = "\t".join(["index", "topic", "application", "Head Summarizer", "LSA", "LexRank", "Luhn", "Edmund", "Gensim" ]) + "\n"
        header = "\t".join(
            ["index", "topic", "application", "Head Summarizer", "LSA", "LexRank", "Luhn", "Edmund"]) + "\n"
        f_out_fact.write(header)
        f_out_news.write(header)
        f_out_opinion.write(header)

        for i, topic in enumerate(topics):
            #print("===========\n" + topic + '\n===========')
            source_article_map = get_articles(topic, reddit_streamer)
            if source_article_map:
                for source, article in source_article_map.items():

                    if source not in source_algo_scores:
                        source_algo_scores[source] = {}


                    #print("---- " + source + ' -----')
                    output = [str(i + 1), topic, source]
                    if len(article.split()) > 50:
                        article_short = article.split()[:50]

                        summaries = get_summaries(article, topic)
                        for algo, summary in summaries.items():
                            #print (algo, ": ", summary)
                            output.append(summary.strip())

                            b, r = get_belu_rouge_score(article_short, summary)

                            #print (b, r)

                            if algo not in source_article_map[source]:
                                source_algo_scores[source][algo] = {}

                            if 'bleu' not in source_algo_scores[source][algo]:
                                source_algo_scores[source][algo]['bleu'] = [b]
                            else:
                                source_algo_scores[source][algo]['bleu'].append(b)

                            if 'rouge' not in source_algo_scores[source][algo]:
                                source_algo_scores[source][algo]['rouge'] = [r]
                            else:
                                source_algo_scores[source][algo]['rouge'].append(r)

                    output = "\t".join(output) + "\n"
                    if source == 'wiki:fact':
                        f_out_fact.write(output)
                    elif source == 'reddit:opinion':
                        f_out_opinion.write(output)
                    else:
                        f_out_news.write(output)
                print ("yo")
                #print()

        print ("done: ", j)


    for source in source_algo_scores:
        print ("============" + source + "==========")
        for algo in source_algo_scores[source]:
            print("-----" + algo + "-----")
            print ("avg bleu: ", np.average(source_algo_scores[source][algo]['bleu']))
            #print ("median bleu: ", np.median(source_algo_scores[source][algo]['bleu']))
            print ("avg rouge: ", np.average(source_algo_scores[source][algo]['rouge']))
            #print ("median rouge: ", np.median(source_algo_scores[source][algo]['rouge']))


    with open('source_algo_scores.pkl', 'wb') as handle:
        pickle.dump(source_algo_scores, handle)

        print ()








