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

def main():
    seek_dict = {}
    length_dict = {}
    title_dict = {}
    counts = {}
    doc_dict = {}
    score = {}

    query = sys.argv[1]
    body_index_file = open('./index/body.txt', 'r')
    file_to_dict("./index/dict_body.txt", seek_dict, 0)
    file_to_dict("./index/length.txt", length_dict, 1)

    print query
    process_query(query, counts)

    for term in counts:
        body_index_file.seek(seek_dict[term], 0)
        line = body_index_file.readline()
        doc_dict = {}
        make_doc_dict(line, doc_dict)

        print len(doc_dict)
        idft = math.log10(len(length_dict)/len(doc_dict))
        tf = 1 + math.log10(counts[term])
        wq = idft * tf
        for doc in doc_dict:
            if doc not in score:
                score[doc] = doc_dict[doc] * wq;
            else:
                score[doc] += (doc_dict[doc] * wq);

        #print score
    ans = []
    for key in sorted(score,key=score.get,reverse=True):
        ans.append([key, score[key]])
        if len(ans)>10:
            break

    file_to_dict("./index/lt.txt", title_dict, 2)
    for elem in ans:
        link = title_dict[elem[0]]
        link=link.replace(' ', '_')
        link= "https://en.wikipedia.org/wiki/"+link
        print elem[0], elem[1], link

if __name__ == "__main__":
    main()
