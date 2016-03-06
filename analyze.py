import os
import json

import lxml.html
import requests
from tqdm import tqdm

movies = {}
critics = {}
criticsURL = {}
stoper = 0
pbar = tqdm(total=59964)
for rootf, dirs, filenames in os.walk('criticdownloads/'):
    for f in filenames:
        if "best" not in f and "worst" not in f:
            continue
        pbar.update(1)
        stoper += 1
        if stoper > 10000000:
            break
        #print(rootf,f)
        fname = os.path.join(rootf, f)
        #print("-"*30)
        #print(fname)
        html = open(fname,'r').read()
        root = lxml.html.fromstring(html)
        critic = root.xpath('//div[@class="panel-body content_body"]/div/div/h2[@class="title"]')[0].text_content().strip()
        if critic not in critics:
            critics[critic] = []
            #var = requests.get(r'http://www.google.com/search?q="%s movie reviews"&btnI' % critic)
            #criticsURL[critic] = var.url
        reviews = root.xpath('//table[@class="table table-striped"]/tr')
        for review in reviews:
            title = review.xpath('.//td/a')[0].text_content().strip()
            year = review.xpath('.//td[@class="center"]')[0].text_content().strip()
            if ("2017" not in year 
                    and "2016" not in year 
                    and "2015" not in year
                    and "2014" not in year
                    and "2013" not in year
                    and "2012" not in year):
                continue
            if title not in movies:
                movies[title] = {}
                movies[title]['good'] = []
                movies[title]['bad'] = []
                movies[title]['rtgood'] = True
            tds = review.xpath('.//td')
            num = 0 
            for td in tds:
                spans = td.xpath('.//span')
                for span in spans:
                    if 'title' in span.attrib:
                        if num == 0:
                            critics[critic].append(title)
                            critics[critic] = list(set(critics[critic]))
                            if ('fresh' in span.attrib['class'].strip()
                                    or 'certified' in span.attrib['class'].strip()):
                                movies[title]['good'].append(critic)
                                movies[title]['good'] = list(set(movies[title]['good']))
                            else:
                                movies[title]['bad'].append(critic)
                                movies[title]['bad'] = list(set(movies[title]['bad']))
                        elif num == 1:
                            movies[title]['rtgood'] = 'rotten' not in span.attrib['class'].strip()
                        num += 1

pbar.close()
with open('movies.json','w') as f:
	f.write(json.dumps(movies,indent=1))
with open('critics.json','w') as f:
	f.write(json.dumps(critics,indent=1))
with open('criticsURL.json','w') as f:
	f.write(json.dumps(criticsURL,indent=1))
