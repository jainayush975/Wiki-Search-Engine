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

def update_page(page_dict, doc_dict, page_id):
    bt=""
    tt=""
    el=""
    ct=""
    rf=""
    for key in page_dict:
        if page_dict[key][0] != 0:
            bt = "b" + str(page_dict[key][0])
        if page_dict[key][1] != 0:
            tt = "t" + str(page_dict[key][1])
        if page_dict[key][2] != 0:
            el = "l" + str(page_dict[key][2])
        if page_dict[key][3] != 0:
            ct = "c" + str(page_dict[key][3])
        if page_dict[key][4] != 0:
            rf = "r" + str(page_dict[key][4])


        if key not in doc_dict:
            doc_dict[key] = "," + str(page_id) + bt + tt + el
        else:
            doc_dict[key] = doc_dict[key] + "," + str(page_id) + bt + tt + el

def find_references(txt, page_dict):
    if txt is not None:
        lines = txt.split("== References ==")
        if len(lines)>1:
            lines = lines[1].split('\n')
            for line in lines:
                if line == "":
                    break
                words = re.split(r'[^A-Za-z]+', line)
                for word in words:
                    if word is not None and word != 'Category' and word != "" and word not in ["Reflist", "colwidth", "em", "ref" ,"refs"]:
                        word = word.lower()
                        word = stem(word)
                        if word not in page_dict:
                            page_dict[word] = [0,0,0,0,1]
                        else:
                            page_dict[word][4] += 1




def find_category(txt, page_dict):
    if txt is not None:
        lines = txt.split('\n')
        for line in lines:
            if '[[Category:' in  line:
                words = re.split(r'[^A-Za-z]+', line)
                for word in words:
                    if word is not None and word != 'Category' and word != "":
                        word = word.lower()
                        word = stem(word)
                        if word not in page_dict:
                            page_dict[word] = [0,0,0,1,0]
                        else:
                            page_dict[word][3] += 1

def external_link(txt, page_dict):
    if txt is not None:
        lines = txt.split("==External links==")
        if len(lines)>1:
            lines = lines[1].split('\n')
            for line in lines:
                if "* [" in line or "*[" in line:
                    words = re.split(r'[^A-Za-z]+', line)
                    for word in words:
                        if word is not None and 'http' not in word and word not in stopwords:
                            word = stem(word)
                            if word not in page_dict:
                                page_dict[word] = [0,0,1,0,0]
                            else:
                                page_dict[word][2] += 1

def title_in_a_page(title, page_dict):
    if title is not None:
        title = re.split(r"[^A-Za-z]+", title);
        for word in title:
            word = word.lower()
            if word not in stopwords:
                word = stem(word)
                if word not in page_dict:
                    page_dict[word] = [0,1,0,0,0]
                else:
                    page_dict[word][1] += 1

def make_for_page(txt, page_dict):
    if txt is not None:
        txt = re.split(r"[^A-Za-z]+", txt);

        for word in txt:
            word = word.lower()
            if word not in stopwords:
                word = stem(word)
                if word not in page_dict:
                    page_dict[word] = [1,0,0,0,0]
                else:
                    page_dict[word][0] += 1

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

for event, element in etree.iterparse(path, events=('start', 'end')):
    tname = strip_tag_name(element.tag)

    if event == "start":
        if tname == "page":
            main_text=""
            title=""
        elif tname == "id":
            if not in_revision and element.text is not None:
                page_id=int(element.text);
        elif tname == "revision":
            in_revision = True
        elif tname == "redirect":
            if bool(element.attrib):
                title = element.attrib['title']
                title_in_a_page(title, page_dict)
    else:
        if tname == "revision":
            in_revision = False
        elif tname == "text":
            main_text = element.text
            find_references(main_text, page_dict)
            find_category(main_text, page_dict)
            external_link(main_text, page_dict)
            make_for_page(main_text, page_dict)
        elif tname == "page":
            update_page(page_dict, doc_dict, page_id)
            page_dict.clear()
    element.clear()

dict_to_string(doc_dict)

#if __name__ == "__main__":
#    main()
