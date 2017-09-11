from stemming.porter import stem
from stopword import stopwords
import re

def strip_tag_name(t):
    #t = element.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

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

def external_link(txt, page_dict):
    if txt is not None:
        lines = txt.split("==External links==")
        if len(lines)>1:
            lines = lines[1].split('\n')
            for line in lines:
                if "* [" in line or "*[" in line:
                    words = re.split(r'[^A-Za-z]+', line)
                    for word in words:
                        word=word.lower()
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

def find_category(txt, page_dict):
    if txt is not None:
        lines = txt.split('\n')
        for line in lines:
            if '[[Category:' in  line:
                words = re.split(r'[^A-Za-z]+', line)
                for word in words:
                    word = word.lower()
                    if word is not None and word != 'Category' and word != "":
                        word = word.lower()
                        word = stem(word)
                        if word not in page_dict:
                            page_dict[word] = [0,0,0,1,0]
                        else:
                            page_dict[word][3] += 1

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
                    word = word.lower()
                    if word is not None and word != 'Category' and word != "" and word not in ["Reflist", "colwidth", "em", "ref" ,"refs"]:
                        word = stem(word)
                        if word not in page_dict:
                            page_dict[word] = [0,0,0,0,1]
                        else:
                            page_dict[word][4] += 1
