import os
import json

import lxml.html

movies = {}
stopper = 0
for rootf, dirs, filenames in os.walk('criticdownloads/'):
    for f in filenames:
        stopper += 1
        if stopper > 1000:
            break
        print(rootf,f)
        fname = os.path.join(rootf, f)
        print("-"*30)
        print(fname)
        html = open(fname,'r').read()
        root = lxml.html.fromstring(html)
        critic = root.xpath('//div[@class="panel-body content_body"]/div/div/h2[@class="title"]')[0].text_content().strip()
        print(critic)
        reviews = root.xpath('//table[@class="table table-striped"]/tr')
        for review in reviews:
            title = review.xpath('.//td/a')[0].text_content().strip()
            if title not in movies:
                movies[title] = {}
                movies[title]['good'] = []
                movies[title]['bad'] = []
                movies[title]['rtgood'] = True
            print(title)
            tds = review.xpath('.//td')
            num = 0 
            for td in tds:
                spans = td.xpath('.//span')
                for span in spans:
                    if 'title' in span.attrib:
                        if num == 0:
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

print(json.dumps(movies,indent=2))