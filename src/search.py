import sys
from stemming.porter import stem
from stopword import stopwords
import re
import math

def file_to_dict(path, out_dict, flag):

    fl = open(path, 'r')
    for line in fl:
        ln = re.split(r'[:\n]',line)
        if flag==0:
            out_dict[ln[0]]=int(ln[1])
        elif flag==2:
            out_dict[int(ln[0])]=(ln[1])
        else:
            out_dict[int(ln[0])]=int(ln[1])

def process_query(query, counts):
    if query is not None:
        words = re.split(r'[^A-Za-z]', query)

        for word in words:
            word = word.lower()
            if word not in stopwords:
                word = stem(word)
                if word not in counts:
                    counts[word]=1
                else:
                    counts[word]+=1
    else:
        raise ValueError("Query provided can't be processed")

def make_doc_dict(line, doc_dict):
    docs = re.split(r'[,]',line)
    for doc in docs[1:]:
        p=re.split(r'[:]', doc)
        doc_dict[int(p[0])] = float(p[1])

def process_body(counts, seek_dict, length_dict, score, body_index_file):
    doc_dict = {}
    for term in counts:
        if term in seek_dict:
            body_index_file.seek(seek_dict[term], 0)
            line = body_index_file.readline()
            doc_dict = {}
            make_doc_dict(line, doc_dict)
            idft = math.log10(len(length_dict)/len(doc_dict))
            tf = 1 + math.log10(counts[term])
            wq = idft * tf
            for doc in doc_dict:
                if doc not in score:
                    score[doc] = doc_dict[doc] * wq;
                else:
                    score[doc] += (doc_dict[doc] * wq);

def main():
    seek_dict = {}
    length_dict = {}
    link_title_dict = {}
    counts = {}
    score = {}
    title_counts = {}
    title_dict = {}
    category_dict = {}
    category_counts = {}
    body_query = ""
    title_query = ""
    category_query = ""

    query = sys.argv[1]
    body_index_file = open('./index/body.txt', 'r')
    title_file = open('./index/title.txt', 'r')
    category_file = open('./index/category.txt', 'r')
    file_to_dict("./index/dict_category.txt", category_dict, 0)
    file_to_dict("./index/dict_title.txt", title_dict, 0)
    file_to_dict("./index/dict_body.txt", seek_dict, 0)
    file_to_dict("./index/length.txt", length_dict, 1)

    print query
    query = re.split(r'[;]', query)
    for q in query:
        if "T:" in q:
            title_query = re.split(r'[:]', q)[1]
        elif "B:" in q:
            body_query = re.split(r'[:]', q)[1]
        elif "E:" in q:
            category_query = re.split(r'[:]', q)[1]
        else:
            body_query = re.split(r'[\n]', q)[0]
            title_query = body_query

    if category_query!="":
        process_query(category_query, category_counts)
        process_body(category_counts, category_dict, length_dict, score, category_file)

    process_query(body_query, counts)       #counts stores the count of each word in query;
    process_query(title_query, title_counts)


    process_body(title_counts, title_dict, length_dict, score, title_file)
    process_body(counts, seek_dict, length_dict, score, body_index_file)

    results = []
    for key in sorted(score,key=score.get,reverse=True):
        results.append([key, score[key]])
        if len(results)>10:
            break

    file_to_dict("./index/lt.txt", link_title_dict, 2)
    for elem in results:
        link = link_title_dict[elem[0]]
        link=link.replace(' ', '_')
        link= "https://en.wikipedia.org/wiki/"+link
        print elem[0], elem[1], link


if __name__ == "__main__":
    main()

    """
    for key in title_score:
        if key in score:
            score[key] += title_score[key]
        else:
            score[key] =  title_score[key]
    """
