readme.md

# some experiments with extracting information out of a subtitle file

Adjust *.env* settings
subtitles_url           = a url to a xml.subtitles file 
extracted_text_file     = filename of extracted contents 
data_folder             = folder where data lives, usually './data/', keep trailing slash

code here is supposed to do the following. 
make sure to run in chronological order via 
python 01...
python 02...

1. 01_extract_textinfo_from_subtitles_xml.py
take a subtitle - xml file (with xmls namspace (Timed Text Markup Language (TTML) 1.0) and extract text content. Text content is saved to a file

2. 02_spacy_term_extraction.py
spacy NER does not realy work with these types of texts. Needs better findtuning. 
Common_words.csv instead seems to be usefull. Its simple lemmatized nouns ordered by their frequency

3. 03_flair_term_extraction.py
Doing Named Entity Exractions with flair library (LINK). switch model in use inside of file. 
is supposed to produce CSV files, named like model, i.e. _flair_ners_german-large.csv


4. 04_aggr_csvs_and_do_some_counting.py
takes results from former steps and aggregates data into a more readable format. It takes Named Entities of type "ORG" and "MISC" out of files produced by step (3)

5. 05_synonyms_from_wikidata.py
Do some SPARQL-Queries in order to get synonyms for terms. 
The term list used here is manually extracted from Website's meta-keywords. 
Produces a CSV-File with Search-Term, Wikidata-Result, Wikidata-URL, Wikidata-ID, Aliases


