# imports
from bs4 import BeautifulSoup
import requests
import validators
import ssl
import urllib3

# set initial data-structures
depth, max_depth =1,3
urls = set() # we use set to maintain distinct urls
new_urls = set() # we use set to maintain distinct urls
completed_urls = []
failed_urls = set()

# get the list of urls from user
user_inputs = ["https://www.rice.edu/"]

# append the urls to urls set
for url in user_inputs:
    urls.add(url)

while depth <= max_depth:
    while (len(urls) != 0): 
        url = urls.pop()
        
        # get url's html content
        try:
            response = requests.get(url)
        except (requests.exceptions.InvalidSchema, ssl.SSLError, urllib3.exceptions.MaxRetryError,
                 requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            failed_urls.add(url)
            continue

        # check if response is valid
        if response.status_code != 200:
            failed_urls.add(url)
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
            if (is_valid_url==True and extracted_url not in completed_urls 
                and extracted_url not in failed_urls and extracted_url != url):
                new_urls.add(extracted_url)

        completed_urls.append(url)

    print("depth: " + str(depth) + ":: new_urls: " + str(len(new_urls)))
    urls = new_urls.copy()
    new_urls.clear()
    depth += 1

print("\ncompleted urls: ")
# print list of completed urls
for url in completed_urls:
    print(url)

print("\nfailed urls: ")
# print list of failed urls
for url in failed_urls:
    print(url)