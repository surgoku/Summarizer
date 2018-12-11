import unidecode
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer

from nlp_lib import tokenize_article_to_sentences, get_wiki_article

from gensim.summarization.summarizer import summarize as gensim_summarizer


from gensim.summarization import keywords


LANGUAGE = "english"
SENTENCES_COUNT = 1
stemmer = Stemmer(LANGUAGE)
stop_words = get_stop_words(LANGUAGE)


def head_summarizer(article):
    article_summary = tokenize_article_to_sentences(article)[0]
    article_summary = unidecode.unidecode(article_summary)
    return article_summary

def get_summaries(article, topic):

    parser = PlaintextParser(article, Tokenizer(LANGUAGE))
    summarizer_list = [head_summarizer, LsaSummarizer, LexRankSummarizer, LuhnSummarizer, EdmundsonSummarizer,
                       ]#gensim_summarizer]  # , lex_rank]
    summarizers_name = ["Head Summarizer", "LSA", "LexRank", "Luhn", "Edmund"]#, "Gensim"]

    summary_dict = {}

    for Summarizer, name in zip(summarizer_list, summarizers_name):
        #rint(name, )
        summary = ''
        if Summarizer == head_summarizer:
            summary = head_summarizer(article)
        elif Summarizer == gensim_summarizer:
            ratio = 0.01
            while len(summary.split()) < 15:
                summary = Summarizer(" ".join(article.split('\n')), ratio=ratio)
                ratio = ratio*5
            if len(summary.split()) > 40:
                summary = tokenize_article_to_sentences(summary)[0]


        elif Summarizer == EdmundsonSummarizer:
            summarizer = Summarizer()
            summarizer.bonus_words = topic.lower().split()
            summarizer.stigma_words = stop_words
            summarizer.null_words = stop_words

            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                summary += str(sentence)

        else:
            summarizer = Summarizer(stemmer)
            summarizer.stop_words = stop_words
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                summary += str(sentence)

        #summary = re.sub("[\(\[].*?[\)\]]", "", summary)
        #summary = " ".join(summary.split())

        if '( listen)' or '(listen)' in summary:
            summary = re.sub('\( listen\)', ' ', summary)

        summary_dict[name] = summary

    return summary_dict


if __name__ == '__main__':

    topic = 'narendra modi'
    article = get_wiki_article(topic)

    summaries = get_summaries(article, topic)

    for k,v in summaries.items():
        print (k)
        print (v)
        print ()
