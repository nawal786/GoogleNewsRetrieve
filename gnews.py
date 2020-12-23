from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


googlenews = GoogleNews(period='1d')


keyword = 'KN95'
googlenews.get_news(keyword)

#print(googlenews.result()[0])
title = []
date = []
gnewsurl = []
site = []
author = []


search_results = len(googlenews.result())
numarticles = 100

if numarticles > search_results:
    numarticles = search_results
    print("Got {0} hits for '{1}'. Crawling {2} results\n".format(search_results, keyword, numarticles))
else:
    print("Got {0} hits for '{1}'. Crawling {2} results\n".format(search_results, keyword, numarticles))

googlenews.results(sort=True)

for i in range(0,numarticles):
    result = googlenews.result()[i]
    title.append(result.get('title'))
    date.append(result.get('date'))

    gurl = result.get('link')
    gurl = gurl.replace("./", "")
    gurl = "https://"+gurl

    gnewsurl.append(gurl)
    site.append(result.get('site'))

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
empty = 0
error = 0
success = 0
j = 1
for each in gnewsurl:
    print("Working... ({0}) - {1} ".format(j, each))
    try:
        article = Article(each)
        article.download()
        article.parse()
        authors = article.authors
        if not authors:
            empty = empty + 1
            author.append("No Author Retrieved. Click on link to manually find author.")
        else:
            #print(article.authors, " - ", each)
            author.append(article.authors)
            success = success + 1
    except:
        #print("Error retrieving info: ", each)
        author.append("Error Retrieving Author. Click on link to manually find author")
        error = error + 1

    j = j+1

pct = 100*success/numarticles

zipped = zip(site,date,author,gnewsurl)
column_names = ["Site", "Date", "Author", "URL"]
df = pd.DataFrame(zipped, columns=column_names)
print("\n")
print(df)

print("\nTotal Articles Retrieved for keyword '{0}': {1}".format(keyword, numarticles))
print("Successfully retrieved authors for {0} articles ({1}% success rate).".format(success,pct))
