"""
Outline:
   We take the Named Entity from CSV-Files and merge them into one Dataframe.
   Also some simple "count" stats are calculated
   Outputs 2 files into data-folder starting with 04_
"""
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')
name = extracted_text_file.replace('.txt', '')

# take results from flair ners
ner_raw = pd.read_csv(data_folder + '03_' + name + '_flair_ners_german-large.csv').fillna("")
bert_raw = pd.read_csv(data_folder + '03_' + name + '_flair_ners_distilbert-ner-germeval14.csv').fillna("")


def do_orgas_or_miscs(orgas_or_miscs="ORG"):
    """Function to count ORG or MISC and set some vars into csv."""
    # take only MISC
    ner = ner_raw[ner_raw['tag'] == orgas_or_miscs]
    # insert count column and apply count of term
    ner.insert(1, 'count_flair_1', ner.groupby(['text'])['text'].transform('count'))
    # in order to merge frames later we remove columns here
    ner = ner.drop('score', 1)
    ner = ner.drop('tag', 1)

    # take only OTHERS (here tagged as OTH not MISCH)
    tag = orgas_or_miscs
    if(orgas_or_miscs == 'MISC'):
        tag = 'OTH'
    bert = bert_raw[bert_raw['tag'] == tag]
    # insert count column and apply count of term
    bert.insert(1, 'count_flair_2', bert.groupby(['text'])['text'].transform('count'))
    # in order to merge frames later we remove columns here
    bert = bert.drop('score', 1)
    bert = bert.drop('tag', 1)

    # merge the 3 frames
    all_3 = pd.concat([ner, bert])
    all_3.insert(3, 'count', all_3.groupby(['text'])['text'].transform('count'))

    # prepare frame for output
    out = all_3.groupby(['text'], axis=0, as_index=False).apply(lambda x: x.max())
    out.fillna(0, inplace=True)
    out.columns.values[0] = orgas_or_miscs
    pd.options.display.float_format = '{:,.0f}'.format
    out = out.sort_values(by=['count'], ascending=False)

    out.to_csv(data_folder + '04_' + 'cleaned_' + orgas_or_miscs + '.csv', index=False)
    return out


# display for notbook only
# display(out.head())
out = do_orgas_or_miscs("ORG")
print(out.to_string(index=False))
out = do_orgas_or_miscs("MISC")
print(out.to_string(index=False))
