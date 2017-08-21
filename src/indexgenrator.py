import os,time,csv
import codecs
import re
import xml.etree.ElementTree as etree
import sys
from stemming.porter import stem
from stopword import stopwords
reload(sys)
sys.setdefaultencoding('utf-8')

PATH = "./../"
FILENAME = "wiki-search-small.xml"

# Used to strip the namespace from the tags.

def dict_to_string(doc_dict):
    with open("output.txt", "a+") as fl:
        for key in doc_dict:
            fl.write(str(key) + doc_dict[key] + "\n")

def update_page(page_dict, title_dict, doc_dict, page_id):
    for key in page_dict:
        if key not in title_dict:
            tl=""
        else:
            tl = "t" + str(title_dict[key])
            title_dict.pop(key)
        if key not in doc_dict:
            doc_dict[key] = "," + str(page_id) + "b" + str(page_dict[key]) + tl
        else:
            doc_dict[key] = doc_dict[key] + "," + str(page_id) + "b" + str(page_dict[key]) + tl
    for key in title_dict:
        if key not in doc_dict:
            doc_dict[key] = "," + str(page_id) + "t" + str(title_dict[key])
        else:
            doc_dict[key] = doc_dict[key] + "," + str(page_id) + "t" + str(title_dict[key])

def title_in_a_page(title, title_dict):
    if title is not None:
        title = re.split(r"[^A-Za-z]+", title);
        for word in title:
            word = word.lower()
            if word not in stopwords:
                word = stem(word)
                if word not in title_dict:
                    title_dict[word]=1
                else:
                    title_dict[word]+=1

def make_for_page(txt, page_dict):
    if txt is not None:
        txt = re.split(r"[^A-Za-z]+", txt);

        for word in txt:
            word = word.lower()
            if word not in stopwords:
                word = stem(word)
                if word not in page_dict:
                    page_dict[word] = 1
                else:
                    page_dict[word] += 1

def strip_tag_name(t):
    t = element.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

path = os.path.join(PATH, FILENAME)
page_id = 0
totalCount = 0
in_revision = False
page_dict = {}
doc_dict = {}
title_dict = {}


for event, element in etree.iterparse(path, events=('start', 'end')):
    tname = strip_tag_name(element.tag)

    if event == "start":
        if tname == "page":
            main_text=""
            title=""
        elif tname == "id":
            if not in_revision:
                if element.text is not None:
                    page_id=int(element.text);
        elif tname == "revision":
            in_revision = True
        elif tname == "redirect":
            if bool(element.attrib):
                title = element.attrib['title']
                title_in_a_page(title, title_dict)
    else:
        if tname == "revision":
            in_revision = False
        elif tname == "text":
            main_text = element.text
            make_for_page(main_text, page_dict)
        elif tname == "page":
            update_page(page_dict, title_dict, doc_dict, page_id)
            page_dict.clear()
            title_dict.clear()
    element.clear()

dict_to_string(doc_dict)

#if __name__ == "__main__":
#    main()
