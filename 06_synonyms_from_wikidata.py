#01_get_wikidata_ids.py
# see https://wikifier.org/info.html

import os
import urllib.parse, urllib.request, json
import pandas as pd
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import os
from dotenv import load_dotenv

load_dotenv() 

extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')
name = extracted_text_file.replace('.txt','');

# some experimenting
file = './data/Heizkosten_Begriffe.txt'
# file = './data/keywords_from_webseite.txt'

sparql = SPARQLWrapper(
    "https://query.wikidata.org/sparql"
)
sparql.setReturnFormat(JSON)

# 1st option, query by preflabel
def sparql_get_synonyms_by_preflabel (word):
    query = """SELECT ?item ?prefLabel ?altLabel WHERE {     
      values ?prefLabel {"%s"@de}     
      ?item rdfs:label ?prefLabel ;     
      skos:altLabel ?altLabel . 
      FILTER (lang(?altLabel)='de')
    }""" % (word)
    sparql.setQuery(query)
    results = sparql.queryAndConvert()
    # print(results)
    return results['results']


def sparql_get_wdid_by_label (word):
    query = """SELECT distinct ?item ?itemLabel WHERE{  
      ?item ?label "%s"@de.  
      ?article schema:about ?item .
      ?article schema:inLanguage "de" .
      ?article schema:isPartOf <https://de.wikipedia.org/>. 
      SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }    
    }""" % (word)
    sparql.setQuery(query)
    results = sparql.queryAndConvert()
    # print(results)
    return results['results']

def wikidata_entry_by_wdid (wdid):
    response = requests.get('https://www.wikidata.org/wiki/Special:EntityData/'+wdid+'.json')
    return json.loads(response.text)

with open(file) as f:
    lines = f.readlines()

# words = lines[0].split(',')
words = lines

columns = ['search-term','result-term','url','wdid','aliases']
count = 0;
rows = []
for word in words:
    print('--------')
    print(count,word)
    # res = sparql_get_synonyms_by_preflabel(word.strip())
    res2 = sparql_get_wdid_by_label(word.strip())
    try:
        item = res2['bindings'][0]
        name = item['itemLabel']['value']
        wdurl = item['item']['value']

        wdid = wdurl.split('/')[-1]
        print ("   ",res2['bindings'][0]['itemLabel']['value'],wdurl, wdid)
        entry = wikidata_entry_by_wdid(wdid)
        aliases = ''
        try:
            print(entry['entities'][wdid]['aliases']['de'])
            aliases = ', '.join([name['value'] for name in entry['entities'][wdid]['aliases']['de']])
            rows.append([word.strip(),name,wdurl,wdid,aliases])
            print(aliases)
        except KeyError:
            pass

    except (KeyError, IndexError):
        rows.append([word.strip(),'','','',''])
        pass
    count += 1

df = pd.DataFrame(rows, columns=columns)
df.to_csv(data_folder+'06_'+name+'_meta_aliases.csv',index=False)
print(df)

