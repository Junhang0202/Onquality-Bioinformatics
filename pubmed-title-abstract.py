#Author:Junkang An
#Email:anjunkang22@163.com#
#Extract article ids from pubmed

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
from time import strftime,gmtime
import time
from tqdm import tqdm
import os 
start_time = time.perf_counter()

data = pd.DataFrame(columns=['title','abstract'])

keyword_list = []
keyword="5+fu+resistence"
suffix_list = ['target']
for suffix in suffix_list:
    keyword_list.append(keyword+"+"+suffix)
    #keyword_list.append(suffix)

result_folder = os.getcwd()+'\\'+keyword
word_name = os.path.exists(result_folder)
# Determine if a file exists: not created
if not word_name:
    os.makedirs(result_folder)

with open (keyword+'-PMID.json',encoding='utf-8') as f:
    json_data = json.load(f)
    for i in tqdm(range(len(keyword_list))):
        pmids = re.findall(r"\d+\.?\d*",str(json_data['value'][keyword_list[i]]))
        for j in range(0,len(pmids)):
            url = 'https://pubmed.ncbi.nlm.nih.gov/{}/'.format(pmids[j])
            print(j)
            url.encode('utf-8').decode('unicode_escape')
            response = requests.get(url)
            bs4  = BeautifulSoup(response.content, 'html.parser')
            title_list = bs4.find_all("h1", class_= "heading-title")
            if len(title_list)==0:
                print(f"Title error:{pmids[j]}")
                continue
            title = title_list[0].text.strip()
            abstract_list=bs4.find_all("div", class_= "abstract-content selected")
            if len(abstract_list)==0:
                print(f"Abstract error: {pmids[j]}")
                continue
            abstract = abstract_list[0].text.strip()
            abstract = abstract.encode('ascii', 'ignore').decode()
            abstract = abstract.replace("\n","")
            data['pmid'] = [pmids[j]]
            data['title'] = [title]
            data['abstract'] = [abstract]
            data = data.set_index('pmid')
            data.to_csv(keyword+'-PMID.csv')
            data.to_json(result_folder+'\\{}.json'.format(pmids[j]),orient='columns')

end_time = time.perf_counter()
using_time = strftime("%H:%M:%S", gmtime(end_time - start_time))
print("Time:{}".format(using_time))
f.close()