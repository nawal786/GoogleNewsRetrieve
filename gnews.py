from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
from datetime import datetime
import tkinter as tk

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def scrape():
    keywords = []
    keywords.append(entry.get())
    number_of_articles = int(num_of_articles.get())
    time = '10d'  # change time period to search within (e.g., '1d' --> articles in the past day, '7d' --> past week)

    googlenews = GoogleNews(period=time)
    # googlenews = GoogleNews(lang="en")

    for keyword in keywords:

        googlenews.get_news(keyword)

        numarticles = number_of_articles
        title = []
        date = []
        gnewsurl = []
        site = []
        author = []

        search_results = len(googlenews.result())

        if numarticles > search_results:
            numarticles = search_results
            print("Got {0} hits for '{1}'. Crawling {2} results\n".format(search_results, keyword, numarticles))
        else:
            print("Got {0} hits for '{1}'. Crawling {2} results\n".format(search_results, keyword, numarticles))

        word = [keyword] * numarticles
        googlenews.results(sort=True)

        for i in range(0, numarticles):
            result = googlenews.result()[i]
            title.append(result.get('title'))
            date.append(result.get('date'))

            gurl = result.get('link')
            gurl = gurl.replace("./", "")
            gurl = "https://" + gurl

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
            print("Searching... ('{0}' : {1}/{2}) - {3} ".format(keyword, j, numarticles, each))
            try:
                article = Article(each)
                article.download()
                article.parse()
                authors = article.authors
                if len(authors) == 1:
                    if authors[0] == "Written By":
                        empty = empty + 1
                        author.append("No Author Retrieved. Click on link to manually find author.")
                elif not authors:
                    empty = empty + 1
                    author.append("No Author Retrieved. Click on link to manually find author.")
                else:
                    # print(article.authors, " - ", each)
                    author.append(article.authors)
                    success = success + 1
            except:
                # print("Error retrieving info: ", each)
                author.append("Error Retrieving Author. Click on link to manually find author")
                error = error + 1

            j = j + 1

        pct = 100 * success / numarticles

        zipped = zip(word, site, date, author, gnewsurl)
        column_names = ["Keyword", "Site", "Date", "Author", "URL"]
        df = pd.DataFrame(zipped, columns=column_names)
        print("\n")
        print(df)

        print("\nTotal Articles Retrieved for keyword '{0}': {1}".format(keyword, numarticles))
        print("Successfully retrieved authors for {0} articles ({1}% success rate).".format(success, pct))
        today = datetime.today()
        date = today.strftime("%b-%d-%Y")
        filename = "gnews_search_results_" + date + ".csv"
        df.to_csv(filename, index=False)

        window.destroy()

def test():
    print("Reached")

    print("term - ", entry.get())

window = tk.Tk()
window.geometry("400x200")
window.title("Google News Scraper")
greeting = tk.Label(text="Enter Keyword(s) [separate by comma if multiple keywords]: ")
greeting.pack()

entry = tk.Entry()
entry.pack()

greeting2 = tk.Label(text="Enter number of articles to search for: ")
greeting2.pack()

num_of_articles = tk.Entry()
num_of_articles.pack()

button = tk.Button(
    text="Search n' Scrape",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command = scrape
)

button.pack()

window.mainloop()


