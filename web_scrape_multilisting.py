import json
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

listing_reviews_list = []

def get_number_pages(parsed_content):
    page_string = parsed_content.find('div', {"class": "page-of-pages"})
    try:
        page_contents = page_string.contents[0]
        pages = re.search("of(.*)$", page_contents.strip()).group(1)
    except:
        pages = 0
    return pages
# go to site/page and return list of text of all reviews on page, and how many pages it is
def yelp_reviews_scraping(biz, page=0, refresh=False):
    # Argument page equals 1 by default
    if page == 0:
        # Visit the home page if page equals 1
        yelp_url = 'https://www.yelp.com/biz/%s' % biz
    else:
        # Change url by different argument
        yelp_url = 'https://www.yelp.com/biz/%s?start=' % biz + str((page)*20)

    url_request = requests.get(yelp_url)
    url_content = url_request.content
    parsed_content = soup(url_content)

    parsed_review_list =[]
    description_list = []

    pages = int(get_number_pages(parsed_content))

    container = parsed_content.find('script', {"type":"application/ld+json"})
    page_contents_json = json.loads(container.contents[0])

    review_list = page_contents_json['review']
    for review in review_list:
        ratingValue = review["reviewRating"]["ratingValue"]
        datePublished = review["datePublished"]
        description = review["description"]
        parsed_review_list.append([biz.encode('utf-8'), int(ratingValue), datePublished.encode('utf-8'), description.encode('utf-8')])
        # description_list.append(description.encode('utf-8'))

    print(description_list)
    return parsed_review_list, pages

# returns a list of yelp biz names based on search page
def yelp_get_biz_names(find_loc = 'Berlin', cflt = 'Chinese', page = 0):
    # Argument page equals 1 by default
    if page == 0:
        # Visit the home page if page equals 1
        yelp_url = 'https://www.yelp.com/search?find_loc=%s&cflt=%s' % (find_loc,cflt)
    else:
        # Change url by different argument
        yelp_url = 'https://www.yelp.com/search?find_loc=%s&cflt=%s&start=' % (find_loc,cflt) + str((page)*10)

    url_request = requests.get(yelp_url)
    url_content = url_request.content
    parsed_content = soup(url_content)

    # parsed_review_list =[]
    listings = []

    pages = int(get_number_pages(parsed_content))
    print(type(parsed_content))

    listings_content = parsed_content.find_all('a', {"class":"biz-name js-analytics-click"})
    for biz in listings_content:
        biz_name = biz.get('href')
        try:
            biz = re.search("biz/(.*)$", biz_name).group(1)
            # print(re.search("biz/(.*)$", biz_name).group(1))
            listings.append(biz)
        except:
            continue
        # listings.append(biz.get('href'))
    return listings, pages

# recursively get all reviews fro all pages for the listing by comparing and passign page number
def get_all_reviews_for_listing(biz, page=0):
    if page == None:
        return
    yelp_reviews_page, review_pages = yelp_reviews_scraping(biz, page=page, refresh=False)
    listing_reviews_list.extend(yelp_reviews_page)
    if page < review_pages:
        page += 1
    else:
        return
    get_all_reviews_for_listing(biz, page)

# Go go x search and get all the reviews for the first 20 restaurants
biz_list = []

for page in range(0,5):
    biz_list.extend(yelp_get_biz_names(find_loc = 'Berlin', cflt = 'Chinese', page = page)[0])

for biz in biz_list:
    get_all_reviews_for_listing(biz)
# get_all_reviews_for_listing('jolly-berlin')

# with open('reviews_list.csv', 'w', newline='\n', encoding='utf8') as f:
#     wr = csv.writer(f, quoting=csv.QUOTE_ALL)
#     wr.writerows(listing_reviews_list)

df = pd.DataFrame(listing_reviews_list, columns=["biz","ratingValue", "datePublished", "description"])
df.to_csv('reviews_list.csv', index=False)

# description_list = zip(listing_reviews_list[4])
#
# count_vect = CountVectorizer()
# X_train_counts = count_vect.fit_transform(description_list.data)
# X_train_counts.shape

# TODOS: Implement Text Vectorizer, Word Cloud,multithreading