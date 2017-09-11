import math
import re

def write_correct_index(current_word, current_index, total_docs, offset, dict_file, text_file):#, title_file, category_file, external_file, reference_file):
    index=""
    if(len(current_index)>0):
        idf = math.log10(total_docs/len(current_index))
        for doc in current_index:
            if doc!="":
                cnts = re.split(r'[.]',doc)
                if cnts[1]!="":
                    tf = 1 + math.log10(int(cnts[1]))
                    wt = tf*idf;
                    index = index + "," + cnts[0] + ":" + str('%.2f' %wt)

    if index!="":
        index = current_word+index+"\n"
        dict_file.write(current_word+":"+str(offset)+"\n")
        text_file.write(index)
        offset+=len(index)
    return offset


def merge_chunks(n, total_docs):
    text_file = open('./index/body.txt','w')
    dict_file = open('./index/dict_body.txt', 'w')

    offset = 0
    to_bring = [1 for j in range(n)]
    notend = [1 for j in range(n)]
    lines = []
    files = [open("./chunks/chunk"+str(i)+".txt", 'r') for i in range(n)]

    while (1):
        i=0
        for fl in files:
            if to_bring[i]==1 and notend[i]==1:
                line = fl.readline()
                if not line:
                    notend[i]=0
                    continue
                wrds = re.split(r'[,\n]+',line);
                lines.append([i]+wrds)
                to_bring[i]=0
            i+=1;

        t=0
        for k in notend:
            t=t+k
        if t==0 and not lines:
            break;

        lines.sort(key = lambda x:x[1])

        current_word = lines[0][1]
        current_index = lines[0][2:]
        to_bring[lines[0][0]] = 1

        for line in lines[1:]:
            if line[1]==current_word:
                current_index = current_index + line[2:]
                to_bring[line[0]] = 1

        lines = [x for x in lines if x[1]!=current_word]

        offset = write_correct_index(current_word, current_index, total_docs, offset, dict_file, text_file)#, title_file, category_file, external_file, reference_file)
