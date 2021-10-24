# imports
from bs4 import BeautifulSoup
import requests
import validators
import ssl
import urllib3
import json

class Crawler:
    # default constructor
    def __init__(self, user_inputs, output_filename):
        # set initial data-structures
        self.user_inputs = user_inputs
        self.depth, self.max_depth =1,2
        self.urls = set() # we use set to maintain distinct urls
        self.new_urls = set() # we use set to maintain distinct urls
        self.completed_urls = []
        self.failed_urls = set()
        self.graph = {}
        self.output_filename = output_filename


    def crawl(self):
        # append the urls to urls set
        for url in self.user_inputs:
            self.urls.add(url)

        while self.depth <= self.max_depth:
            while (len(self.urls) != 0): 
                url = self.urls.pop()
                
                # get url's html content
                try:
                    response = requests.get(url)
                except (requests.exceptions.InvalidSchema, ssl.SSLError, urllib3.exceptions.MaxRetryError,
                        requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                    self.failed_urls.add(url)
                    continue

                # check if response is valid
                if response.status_code != 200:
                    self.failed_urls.add(url)
                    continue

                # use beautiful soup object to extract all hyperlinks
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a'):
                    extracted_url = link.get('href')

                    # In some cases, the extracted_url may be None, if so these invalid links shouldnt be processed
                    if not isinstance(extracted_url, str):
                        continue
                    
                    is_valid_url = validators.url(extracted_url)

                    # if extracted links is valid and not in completed_urls and not equal to url, add to new_urls
                    if (is_valid_url==True  
                        and extracted_url not in self.failed_urls and extracted_url != url):
                        self.new_urls.add(extracted_url)

                self.completed_urls.append(url)
                self.graph[url] = self.new_urls

            # print("depth: " + str(self.depth) + ":: new_urls: " + str(len(self.new_urls)))
            self.new_urls = set([page for page in self.new_urls if page not in self.completed_urls])
            self.urls = self.new_urls.copy()
            self.new_urls.clear()
            self.depth += 1


        # print("\ncompleted urls: ")
        # # print list of completed urls
        # for url in self.completed_urls:
        #     print(url)

        # print("\nfailed urls: ")
        # # print list of failed urls
        # for url in self.failed_urls:
        #     print(url)

        # print("\ngraph output: ")
        # print(self.graph)
        self.graph = {k: list(v) for k, v in self.graph.items()}
        with open(self.output_filename, 'w') as fp:
            json.dump(self.graph, fp)


c= Crawler(["https://www.rice.edu/"], "crawler_result.json")
c.crawl()