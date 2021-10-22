


# imports
from bs4 import BeautifulSoup
import requests
import validators

# set initial data-structures
depth, max_depth =1,10
urls = set() # we use set to maintain distinct urls
new_urls = set() # we use set to maintain distinct urls
completed_urls = []

# get the list of urls from user
user_inputs = ["https://stackoverflow.com/"]

# append the urls to urls set
for url in user_inputs:
    urls.add(url)

while depth <= max_depth:
    while (len(urls) != 0): 
        url = urls.pop()

        # get url's html content
        r = requests.get(url)

        # use beautiful soup object to extract all hyperlinks
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a'):
            extracted_url = link.get('href')

            # In some cases, the extracted_url may be None, if so these invalid links shouldnt be processed
            if not isinstance(extracted_url, str):
                continue
            
            is_valid_url = validators.url(extracted_url)

            # if extracted links is valid and not in completed_urls and not equal to url, add to new_urls
            if is_valid_url==True and extracted_url not in completed_urls and extracted_url != url:
                new_urls.add(extracted_url)

        completed_urls.append(url)

    print("old: " + str(len(urls)) + ", new: " + str(len(new_urls)))
    urls = new_urls.copy()
    new_urls.clear()
    depth += 1

# print list of completed urls
for url in completed_urls:
    print(url)