"""
Same as 06_synonyms_from_wikidata.py but uses generated terms for wikidata queries
the generated terms are from 05_{NAME}_map_part_to_common.csv
produces 07_{NAME}_wikifikation_meta_aliases.csv
"""
import os
import urllib.parse, urllib.request, json
import pandas as pd
import numpy as np
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv

load_dotenv()

extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')
name = extracted_text_file.replace('.txt', '')

# some experimenting
# file = './data/Heizkosten_Begriffe.tx
# file = './data/keywords_from_webseite.txt'
file = data_folder + '05_' + name + '_map_part_to_common.csv'

sparql = SPARQLWrapper(
    "https://query.wikidata.org/sparql"
)
sparql.setReturnFormat(JSON)


def sparql_get_synonyms_by_preflabel(word):
    """1st option, query by preflabel."""
    query = """SELECT ?item ?prefLabel ?altLabel WHERE {
      values ?prefLabel {"%s"@de}
      ?item rdfs:label ?prefLabel;
      skos:altLabel ?altLabel .
      FILTER (lang(?altLabel)='de')
    }""" % (word)
    sparql.setQuery(query)
    results = sparql.queryAndConvert()
    # print(results)
    return results['results']


def sparql_get_wdid_by_label(word):
    """Other query return wdid also."""
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


def wikidata_entry_by_wdid(wdid):
    """Wikidata info of a term / wdid."""
    response = requests.get('https://www.wikidata.org/wiki/Special:EntityData/' + wdid + '.json')
    return json.loads(response.text)


# read a csv file into dataframe, take 10 "most occurances"
df = pd.read_csv(file).fillna("").sort_values('num_similiar', ascending=False)[:60]

#  make a set / unique from words in "similar"
words = []
for line in df['similar']:
    for word in line.split(','):
        words.append(word.strip())
# make entries unique / as set
uniques = np.unique(words)

print('Anzahl ', len(uniques))
columns = ['search-term', 'result-term', 'url', 'wdid', 'aliases']
count = 0
rows = []
for word in uniques:
    print('--------')
    print(count, word)
    pass
    res2 = sparql_get_wdid_by_label(word.strip())
    try:
        item = res2['bindings'][0]
        label = item['itemLabel']['value']
        wdurl = item['item']['value']

        wdid = wdurl.split('/')[-1]
        print("   ", res2['bindings'][0]['itemLabel']['value'], wdurl, wdid)
        entry = wikidata_entry_by_wdid(wdid)
        aliases = ''
        try:
            print(entry['entities'][wdid]['aliases']['de'])
            aliases = ', '.join([label['value'] for label in entry['entities'][wdid]['aliases']['de']])
            rows.append([word.strip(), label, wdurl, wdid, aliases])
            print(aliases)
        except KeyError:
            pass

    except (KeyError, IndexError):
        rows.append([word.strip(), '', '', '', ''])
        pass
    count += 1

df = pd.DataFrame(rows, columns=columns)
df.to_csv(data_folder + '07_' + name + '_wikifikation_meta_aliases.csv', index=False)
print(df)
