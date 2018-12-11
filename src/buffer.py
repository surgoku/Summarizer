import codecs

f_fact = codecs.open("../data/topic_summaries_fact_output.txt", 'r', encoding='utf-8')
f_news = codecs.open("../data/topic_summaries_news_output.txt", 'r', encoding='utf-8')
f_op = codecs.open("../data/topic_summaries_opinion_output.txt", 'r', encoding='utf-8')

f_out_fact = codecs.open('../data/to_annotate/topic_summaries_fact_output.txt', 'w', encoding='utf-8')
f_out_news = codecs.open('../data/to_annotate/topic_summaries_news_output.txt', 'w', encoding='utf-8')
f_out_op = codecs.open('../data/to_annotate/topic_summaries_opinion_output.txt', 'w', encoding='utf-8')


annotation_line = "natural\n" + "coherent\n" + "is_summary\n" + "\n"

for line in f_fact:
	f_out_fact.write(line)
	f_out_fact.write(annotation_line)

for line in f_news:
	f_out_news.write(line)
	f_out_news.write(annotation_line)

for line in f_op:
	f_out_op.write(line)
	f_out_op.write(annotation_line)
