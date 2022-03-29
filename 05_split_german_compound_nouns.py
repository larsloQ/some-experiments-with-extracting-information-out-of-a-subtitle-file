"""
Outline:
    script takes the list of lemmatized nouns (see step 2).
    german compound-words (zusammengesetzte Substantive) are splitted into their components
    ("Gasheizung" -> "Gas","Heizung"). This is done via
    script Splitter from here https://github.com/dtuggener/CharSplit
    We save the components into a Dataframe.
    In a second step, we take each component and count its occurance in all compounds.
    Might be usefull for autocompletion
    Two files are save into data Folder:
    1. 05_{NAME}_compounds.csv: "Gas","Heizung","Gasheizung"
    2. 05_{NAME}_map_part_to_common.csv: "Gas","Gasheizung", "Gasrechnung, Gaspreise, Gasverbrauch, Gaspreisen", 4

"""
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from helpers.splitter import Splitter

load_dotenv()

extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')
name = extracted_text_file.replace('.txt', '')


splitter = Splitter()

# take results from spacy lemmatized nouns
df = pd.read_csv(data_folder + '02_' + name + '_spacy_common_words.csv').fillna("")

count = 0
columns = ['part_1', 'part_2', 'compound']
as_parts = []
for index, row in df.iterrows():
    count = count + 1
    compound = row['lemma']
    splitted = splitter.split_compound(compound)
    print (count, '--------', compound, '--------')
    # for reasonable in splitted:
    if splitted[0][0] > .5:
        parts = [p for p in splitted[0][1:3]]
        parts.append(compound)
        as_parts.append(parts)

compounds = pd.DataFrame(as_parts, columns=columns)


compounds.to_csv(data_folder + '05_' + name + '_compounds.csv', index=False)

columns = ['part', 'compound', 'similar', 'num_similiar']
rows = []
# # boolean_finding = df['a'].str.contains('diana').any()
for index, orow in compounds.iterrows():
    # count how often each part is in whole df
    p1 = orow['part_1']
    hits = compounds.loc[compounds.compound.str.contains(p1, case=False)]['compound'].tolist()
    rows.append([p1, orow['compound'], ", ".join(hits), len(hits)])
    p2 = orow['part_2']
    hits = compounds.loc[compounds.compound.str.contains(p2, case=False)]['compound'].tolist()
    rows.append([p2, orow['compound'], ", ".join(hits), len(hits)])


df = pd.DataFrame(rows, columns=columns)
df.to_csv(data_folder + '05_' + name + '_map_part_to_common.csv', index=False)
print(df)
