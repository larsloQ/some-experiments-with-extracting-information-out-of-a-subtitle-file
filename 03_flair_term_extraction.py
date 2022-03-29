"""
Outline:
    - script uses model 'flair/ner-german-large' or 'dbmdz/flair-distilbert-ner-germeval14' 
      to do Named Entity Recognition (NER) 
    - procudes csv-file with all recognized entities './data/03_ners_{model name}.csv'
    - csv file will be use in subsequent scripts to do some analysis
    - check your RAM (with htop or similar). Specially 'flair/ner-german-large' needs some GBs of RAM
"""
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

splitter = SegtokSentenceSplitter()

extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')
subtitle_file = data_folder + "01_" + extracted_text_file
name = extracted_text_file.replace('.txt', '')

# model 1
# we need to run this one after the other, since it uses a lot of memory / RAM
# modelname = 'flair/ner-german-large'
# outfile = data_folder + '03_' + name + '_flair_ners_german-large.csv'

# model 2
modelname = 'dbmdz/flair-distilbert-ner-germeval14'
outfile = data_folder + '03_' + name+'_flair_ners_distilbert-ner-germeval14.csv'

with open(subtitle_file) as f:
    text = f.read()

# use splitter to split text into list of sentences
sentences = splitter.split(text)

tagger = SequenceTagger.load(modelname)

ners = []

for sentence in sentences:
    tagger.predict(sentence)
    # print('-------------NER-----------------------------')
    # print(sentence.to_dict(tag_type='ner'))
    for entity in sentence.get_spans('ner'):
        ners.append([
            entity.text,
            entity.tag,
            entity.score
        ])

# make and export dataframe
df = pd.DataFrame(ners, columns=['text', 'tag', 'score'])
df.to_csv(outfile, index=False)
