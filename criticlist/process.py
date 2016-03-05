import lxml.html

for letter in list('abcdefghijklmnopqrstuvwxyz'):
    html = open('authors?view=3&letter='+letter,'r').read()
    root = lxml.html.fromstring(html)
    hrefs = root.xpath('//table/tr/td/p/a')
    for href in hrefs:
        print 'http://www.rottentomatoes.com' + href.attrib['href'] + 'worst'
        for num in '2 3'.split():
            print 'http://www.rottentomatoes.com' + href.attrib['href'] + 'worst?cats=&genreid=&letter=&switches=&sortby=&limit=50&page=' + num
        print 'http://www.rottentomatoes.com' + href.attrib['href'] + 'best'
        for num in '2 3'.split():
            print 'http://www.rottentomatoes.com' + href.attrib['href'] + 'best?cats=&genreid=&letter=&switches=&sortby=&limit=50&page=' + num

