# some experiments with extracting information out of a subtitle file

Each file here produces one ore more *.csv* files into *data* folder.
These files usually are used in subsequent files. So make sure to run files in chronological order.
For further info see inline-documenation.

See jupyter notebook for some interpreations of results (in German)


## Howto
- install requirements (python -m pip install -r requirements.txt) 
- setup .env variable
- run files in chronological order

## Adjust *.env* settings
subtitles_url           = a url to a xml.subtitles file 
extracted_text_file     = filename of extracted contents 
data_folder             = folder where data lives, usually './data/', keep trailing slash


1. 01_extract_textinfo_from_subtitles_xml.py
take a subtitle - xml file (with xmls namspace (Timed Text Markup Language (TTML) 1.0) and extract text content. Text content is saved to file *1_{NAME}.txt* 
*Make sure to run this step, since the results of step 1) are not in repo, due to some copyright concerns.*

2. 02_spacy_term_extraction.py
spacy NER does not realy work with these types of texts. Needs better findtuning. 
Common_words.csv instead seems to be usefull. Its simple lemmatized nouns ordered by their frequency

3. 03_flair_term_extraction.py
Doing Named Entity Exractions with flair library (LINK). switch model in use inside of file. 
is supposed to produce CSV files, named like model, i.e. _flair_ners_german-large.csv

4. 04_aggr_csvs_and_do_some_counting.py
takes results from former steps and aggregates data into a more readable format. It takes Named Entities of type "ORG" and "MISC" out of files produced by step (3)

5. 05_split_german_compound_nouns.py
splits german compound words ((zusammengesetzte Substantive)) into their parts.  
e.g. "Gasheizung" -> "Gas","Heizung"

6. 06_synonyms_from_wikidata.py
Do some SPARQL-Queries in order to get synonyms for terms. 
The term list used here is manually extracted from Website's meta-keywords. 
Produces a CSV-File with Search-Term, Wikidata-Result, Wikidata-URL, Wikidata-ID, Aliases

7. 07_synonyms_from_wikidata_with_results_from_05.py
same as 6) but terms are extracted from files from steps 2) and 5)


# About
Experiments with some NLP-Tools.  
Any hints welcome.
me@larslo.de



