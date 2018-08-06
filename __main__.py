import bs4
import requests
import os
from wordcloud import WordCloud


def main():
    text = ""
    job = "indeed_machine_learning_engineer"
    get_texts(job)
    for f in os.listdir(job):
        filename = os.path.join(os.path.abspath("."), job, f)
        text += open(filename, "r", errors="ignore").read()
    joined_txt = (" ".join(text.split()))
    wordcloud = WordCloud().generate(joined_txt)
    wordcloud.to_file(job+"_cloud.png")


def get_data_from_indeed(job):
    search_query = " ".join(job.split("_"))
    url = "https://www.indeed.com/jobs"
    all_urls = []
    for page in [0]:
        params = {"start": 0, "q": search_query}
        html_page = requests.get(url, params=params).text
        
        soup = bs4.BeautifulSoup(html_page, features="html.parser")
        urls_ = soup.findAll("a", {"class": "turnstileLink"})
        #print(urls_)
        urls = filter(lambda x: not x.startswith("/cmp") and not x.startswith("/pagead"), list(map(lambda x: x.attrs["href"], urls_)))
        urls = list(urls)
        all_urls.extend(urls)

    
    all_urls = all_urls[:1]
    print(all_urls)
    for i, url in enumerate(all_urls):
        html_page = requests.get("https://www.indeed.com" + url).text
        open("x.html", "w").write(html_page)
        soup = bs4.BeautifulSoup(html_page, features="html.parser")

        try:
            job_text = soup.find("span", {"id": "job_summary"}).text
            
            with open(f"{job}/job_{i}", "w") as f:
                f.write(job_text)
        except AttributeError as e:
            print(e)
            pass


def get_data_from_ziprecruiter(job):
    search_query = " ".join(job.split("_"))
    url = "https://www.ziprecruiter.com/candidate/search"
    all_urls = []
    for page in range(1, 25):
        params = {"page": page, "search": search_query}
        html_page = requests.get(url, params=params).content
        soup = bs4.BeautifulSoup(html_page, features="html.parser")
        urls_ = soup.findAll("a", {"class": "job_link"})
        urls = list(map(lambda x: x.attrs["href"], urls_))
        all_urls.extend(urls)

    for i, url in enumerate(all_urls):
        html_page = requests.get(url).content
        soup = bs4.BeautifulSoup(html_page, features="html.parser")
        try:
            job_text = soup.find("article", {"id": "job_desc"}).text
            with open(f"{job}/job_{i}", "w") as f:
                f.write(job_text)
        except AttributeError as e:
            print(e)
            pass

def get_texts(job):
    try:
        os.mkdir(job)
    except OSError as e:
        pass
    get_data_from_indeed(job)


if __name__ == "__main__":
    main()