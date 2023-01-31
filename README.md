
# directory structure
```
meta
channel-id/
    info
    meta
    comments/
        meta
        comment-id
        ....
    videos/
        video-id
        ....
....
```
so meta will container itterators and other parts useful for picking up where we left off
info file will contain the scrapped info of the channel

# process
## authenticate
- [implementation](https://developers.google.com/identity/protocols/oauth2/service-account#python)
## startup/initalize
- detect where we are in the current data set
## start scraping (we will do syncronus scrapping since this will get us the most data right aways)
    1) fetch counter/list for processing 
        1) walk through api process
        2) store useful data 
        3) move to next counter
    2) update meta files and fetch next process


note we can use some api's to look for legistation data
https://www.congress.gov/help/using-data-offsite
https://legiscan.com/legiscan

# data mining
so we have a couple parts to this 
## text mining 
- analyze transcripts and comments using nlp techniques 
- sentiment analysis, topic modeling and word frequencey 
## data visualization 
- graphs charts maps.....

# Data buckets
mr stack wants me to analyze
- total subscribers (historical or not)
- total videos
- age of account
- how many accounts they are following
- video length
- number of likes
- number of comments
- comments themselves
- transcripts

what I can do/want to do
sentiment analisis
- reffrence laws
- reffrence real laws
- community reception (postive or negative)
    nlg
- scrap extenral sites and just list them
    create like a word bubble

so how dose nlp work?
it uses modules of [ai data](https://www.nltk.org/nltk_data/)
to determine context of senstences so a sentince like 
"that was a very engaging video" would be recored as postive 
"that was a very repuslive video" would be recored as negative
it dose this a bit better as things go on,
we can also use this to detect [textual aggression](https://aclanthology.org/W18-4421.pdf)
so based on a several sources we can determine if content is postive or negative

# NLTK
[nltk](https://www.nltk.org/)
[good tut](https://realpython.com/python-nltk-sentiment-analysis/#getting-started-with-nltk)
[lets dive in](https://www.guru99.com/nlp-tutorial.html)

so there are several components of nlp
- inputs 
- morphological and lexical analysis
    this gets words for analyisis it sperates nonwords from words
- semantic analysis
    this extracts meaning
- pragmatic analysis
    it drerives communicative and social content and its effect on interpretation
    it abstracts meaning or derives meaniful use of language in situations
    the main focus is to reinterpret what is ment
- syntax analysis
    its the rules that govern the sentence structure of any indiviual language
    the smallest unit is a word here for context
- discourse integration
    no clue

# tokenization
so lets chat about tokenizeation 
there are two types 
word tokenize and sentence tokenize 
one works off one then the other
short and sweet it makes analyisis of large words fast

# POS Tagging
it is the process of breaking down a sentince
so NLTK has several tags this is stuff like
nouns... verbs ...




