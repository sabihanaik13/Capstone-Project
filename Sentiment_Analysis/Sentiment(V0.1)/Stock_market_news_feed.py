
import csv
import time
import requests
from bs4 import BeautifulSoup
from pattern.en import ngrams

Base_url = "http://www.moneycontrol.com"


companies = {'cadilahealthcare':'CHC','piramalenterprises':'PH05',
             'glenmarkpharma':'GP08','glaxosmithklinepharmaceuticals':'GSK',
             'sunpharmaceuticalindustries':'SPI','lupinlaboratories':'LL',
             'cipla':'C','aurobindopharma':'AP',
             'drreddyslaboratories':'DRL','divislaboratories':'DL03'}
             
url_list = ['http://www.moneycontrol.com/company-article/{}/news/{}#{}'.format(k,v,v) for k,v in companies.items()]
print(url_list)


List_of_links = []   

for urls in url_list:
    html = requests.get(urls)
    soup = BeautifulSoup(html.text,'html.parser')

    word1,word2,word3 = "US","USA","USFDA"
 
    sub_links = soup.find_all('a', class_='arial11_summ')
    for links in sub_links:
        sp = BeautifulSoup(str(links),'html.parser')  # first convert into a string
        tag = sp.a
        if word1 in tag['title'] or word2 in tag['title'] or word3 in tag['title']:
            category_links = Base_url + tag["href"]
            List_of_links.append(category_links)
            time.sleep(3)


import json

unique_links = list(set(List_of_links))
for q in unique_links: 
    print(q)

for selected_links in unique_links:
    results_url = selected_links 

    results = requests.get(results_url)
    results_text = BeautifulSoup(results.text , "lxml")
    extract_text = results_text.find(class_='arti-flow')
    try:
        data = json.loads(results_text.find('script', type='application/ld+json').text)
    except:
        continue

    final_text = data['description']

    final_text1 = ngrams(final_text, n=1, punctuation=".,;:!?()[]{}`''\"@#$^&*+-|=~_", continuous=False)
    print (final_text1)
    

