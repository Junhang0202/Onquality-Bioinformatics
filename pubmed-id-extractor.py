#Author:Junkang An
#Email:anjunkang22@163.com
#Extract article ids from pubmed
#Limited 1000 results for each keyword (more details:https://pubmed.ncbi.nlm.nih.gov/help/#10k-results)
#Better to use the institution's VPN to crawling

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import math
import time
from time import strftime,gmtime

start_time = time.perf_counter()

keyword_list = []
keyword="5+fu+resistence"

suffix_list = ['target']
#suffix_list=["Mno2","absorption","adsorption", "detection", "sensing", "determination", "sensor", "remove", "degradation", "oxidation"]
out = []

#Making the keyword list
for suffix in suffix_list:
    keyword_list.append(keyword+"+"+suffix)
    #keyword_list.append(suffix)

#First, find page numbers by keyword_list
for i in range(len(keyword_list)):
    urls = ['https://pubmed.ncbi.nlm.nih.gov/?term={}'.format(keyword_list[i])]
    for url in urls:
        response = requests.get(url)
        bs4  = BeautifulSoup(response.content, 'html.parser')
        pages = bs4.find('div',{'class':'results-amount'})
        page = pages.text
        result = re.findall(r"\d+",page)
        if len(result) == 1:
            result = str(result)
            result_number = int(result[2:-2])
        else:
            print("搜索结果超过1000条")
            a = []
            a.append(result[0]+result[1])
            result = str(a).replace(',','')
            result_number = int(result[2:-2])
            page = math.ceil(result_number/200)

        if page > 6:
            page = 5
            print(keyword_list[i],page)
        for p in range(1,page+1):
            full_urls = ['https://pubmed.ncbi.nlm.nih.gov/?term={}&filter=simsearch1.fha&page={}&format=pmid&size=200'.format(keyword_list[i], p)]
            for full_url in full_urls:
                r = requests.get(full_url)
                soup  = BeautifulSoup(r.content, 'lxml')
                try:
                    pmid_list = soup.find('pre').text
                    pmidlist = pmid_list.split('\r\n')
                except:
                    print("{} exceeded the 1000 list limit".format(keyword_list[i]))
                finally:
                    out.append(keyword_list[i]+":"+str(pmid_list))
                    
file = open('a.txt', 'w')
for i in range(len(out)):
    s = str(out[i]).replace('\r\n',' ').replace(':',' ')+' '
    file.write(s+'\n')
file.close()

f=open("a.txt")
ha={}
key = []
value = []
for i in f:
    i=i.strip().split()
    for k in i[1:]:
        ha.setdefault(i[0],[]).append(k)
for k in ha:
    a = list(set(ha[k]))
    print(k)
    key.append(k)
    value.append(a)
    #Transfer pandas to JSON
    data = pd.DataFrame(columns=['key','value'])
    data['key'] = key
    data = data.set_index('key')
    data['value'] = value
    data.to_json('5-fu-resistance-target-PMID.json',orient='columns')

end_time = time.perf_counter()
using_time = strftime("%H:%M:%S", gmtime(end_time - start_time))
print("Time:{}".format(using_time))
