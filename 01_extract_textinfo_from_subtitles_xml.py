# -*- coding: UTF-8 -*-

"""

1. 01_extract_textinfo_from_subtitles_xml.py
take a subtitle - xml file (with xmls namspace (Timed Text Markup Language (TTML) 1.0) and extract text content. 
Text content is saved to a file with name from *extracted_text_file*

"""

import xml.etree.ElementTree as ET
import requests
import os
from dotenv import load_dotenv
import codecs

load_dotenv()

subtitles_url = os.environ.get('subtitles_url')
extracted_text_file = os.environ.get('extracted_text_file')
data_folder = os.environ.get('data_folder')

response = requests.get(subtitles_url)

# xmls namspace (Timed Text Markup Language (TTML) 1.0,
# required due to namespaced elements
ns = {'tt': 'http://www.w3.org/ns/ttml'}
root = ET.fromstring(response.text)

# write contents to a file for later analysis.
# its adds newlines after each subtitle / panel.
text_contents = codecs.open(data_folder + "01_" + extracted_text_file, 'w', encoding="utf-8")

spans = root.findall('tt:body/tt:div/tt:p/tt:span', ns)

words = 0
chars = 0
lines = 1
for span in spans:
    text_contents.write(span.text)
    if(span.text.rstrip()[-1] == '.'):
        text_contents.write('\n')
        lines = lines + 1
    else:
        text_contents.write(' ')

    chars = chars + len(span.text)
    words = words + len(span.text.split(" "))

print("-----------------")
print("File contains {} lines with {} words and {} characters".format(lines, words, chars))
print("-----------------")
print("First 15 lines:")
for span in spans[0:15]:
    print("  " + span.text)
print("-----------------")
print("File saved to {}".format(data_folder + extracted_text_file))
print("-----------------")

text_contents.close()
