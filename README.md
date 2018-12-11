## Evaluating Summarization Algorithms for Voice Assistants
---

In this project, we analyzed various summarization algoriths for voice Assistants such as Alexa. We build three kinds of chatbots: 
* Information Bot
* News Bot
* Opinion Bot

Alexa users interact with these chatbots, which summarize the articles for any topic provided by the user. The chatbots are built to obtain data corresponding to each source. For News we use NEWSAPI.ORG, for opinion bot we use Reddit, and for Information Bot we use WIkipedia as the knowledge source. We summarize the articles using the following summarization algorithms for each of these use cases:

* Luhn
* LSA
* LexRank
* Head Summarizer
* Edmundson Summarizer


All the code for summarizer and the bot that we have built can be found under "src" folder.


We evaluate the summarizers using Quantitative Metrics such as BLEU and ROUGE as well as Qualitative metrics such as: Coherence, Naturalness, etc.