from lxml.html import fromstring
import requests
import csv

def parse_doc(doc):
    items_xpath='//div[@class="panel-body content_body"]/div[count(preceding-sibling::hr)=0]'
    for item in doc.xpath(items_xpath):
        original_url=item.xpath('a/@href')
        original_url=url_prefix+original_url[0] if original_url else ''
        #print original_url
        img_source=item.xpath('a/img/@src')
        img_source=img_source[0] if img_source else ''
        description_text=item.xpath('div/p//text()')
        #print ''.join(description_text)
        description_text=description_text if description_text else []
        description_text=''.join(description_text)
        if not description_text:
            continue
        #original_url[len(original_url)/2-7:len(original_url)/2+7]='DEMONSTRATION'
        original_url=original_url[:len(original_url)/2-7]+'DEMONSTRATION'+original_url[len(original_url)/2+7:]

        #img_source[len(img_source)/2-7:len(img_source)/2+7]='DEMONSTRATION'
        img_source=img_source[:len(img_source)/2-7]+'DEMONSTRATION'+img_source[len(img_source)/2+7:]
        #for i in xrange(0,len(description_text-13),30):
        #    description_text[i:i+14]='DEMONSTRATION'
        yield [original_url,img_source,description_text]

url_prefix='http://www.rottentomatoes.com'
url='http://www.rottentomatoes.com/news/columns/five_favorite_films'
response=requests.get(url)
doc=fromstring(response.content.decode('latin-1'))
PAGES_XPATH='//div[@class="clearfix bottom_divider"]/div/div[2]/span[count(following-sibling::span)=0]/a/text()'
pagecount=int(doc.xpath(PAGES_XPATH)[0])

print 'Total {} pages.'.format(pagecount)
with open('result.csv','wb') as outfile:
    writer=csv.writer(outfile)
    writer.writerow(['Original URL','Image URL','Description text'])
    for line in parse_doc(doc):
        writer.writerow(map(lambda x:x.encode('utf-8'),line))
    for pagenum in xrange(2,pagecount+1):
        print "Processing page {:2} ".format(pagenum),
        url='http://www.rottentomatoes.com/news/columns/five_favorite_films?page={}'.format(pagenum)
        response=requests.get(url)
        doc=fromstring(response.content.decode('latin-1'))
        for line in parse_doc(doc):
            writer.writerow(map(lambda x:x.encode('utf-8'),line))
        print "done."
