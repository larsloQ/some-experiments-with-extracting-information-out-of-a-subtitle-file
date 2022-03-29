# 01_term_frequency.py

"""
    Outline:
    - extract information about the text from 01.
     This is done by using spacy (https://github.com/explosion/spaCy/)

    - the script exports
    -- all lemmatized NOUNs
    -- all ORG-Entities spacy found (Organizations)
    -- all MISC-Entities spacy found (miscellaneous)

    - since the computation is rather heavy
     script saves the results into csv's in ./data folder (nouns,orgas,miscs)

    to make spacy running see https://github.com/explosion/spaCy/
    the used model 'de_core_news_lg'
    is about 550 MB and needs to be downloaded before running this via
    *python -m spacy download de_core_news_lg*
"""

import spacy
import pandas as pd
from collections import Counter
import os
from dotenv import load_dotenv

# from spacy import displacy, visualize results on a webpage, see end of file

load_dotenv()


extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')
subtitle_file = data_folder + '01_' + extracted_text_file
name = extracted_text_file.replace('.txt', '')

with open(subtitle_file) as f:
    text = f.read()

# run *python -m spacy download de_core_news_lg* once
# model is around 550 MB
nlp = spacy.load('de_core_news_lg')

doc = nlp(text)
print('----------------------------------------')
# print(list(doc.sents)[0])

# spacy.displacy.render(doc, style="ent")
# all tokens that arent stop words or punctuations
nouns = [token.lemma_ for token in doc
         if not token.is_stop and not token.is_punct and token.pos_ == "NOUN"]

# verbs = [token.lemma_ for token in doc
#          if not token.is_stop and not token.is_punct and token.pos_ == "VERB"]

orgas = [ent for ent in doc.ents
         if ent.label_ == "ORG"]

miscs = [ent for ent in doc.ents
         if ent.label_ == "MISC"]


lemma_freq = Counter(nouns)
common_words = lemma_freq.most_common(300)
df_nouns = pd.DataFrame(common_words, columns=['lemma','count'])
df_nouns.to_csv(data_folder + '02_' + name + '_spacy_common_words.csv',index=False)
print('common words')
print(common_words, len(common_words))


df = pd.DataFrame(orgas)
print('----------------------')
print('Organisation Entities, saved to file "data/.._spacy_orgas.csv"')
df.to_csv(data_folder + '02_' + name + '_spacy_orgas.csv', index=False)
'--------'
miscdf = pd.DataFrame(miscs)
print('----------------------')
print('Misc Entities, saved to file "data/..._spacy_miscs.csv"')
print(miscdf.head())
miscdf.to_csv(data_folder + '02_' + name + '_spacy_miscs.csv', index=False)

#  ------------VISUALIZE --------------------------------
# inside noteboock
# displacy.render(doc, style="ent")
# outside noteboock
# displacy.serve(doc, style="ent")