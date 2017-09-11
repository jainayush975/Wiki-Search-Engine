import os,time,csv
import codecs
import re
import xml.etree.ElementTree as etree
import sys
from parser import strip_tag_name, make_for_page, external_link, title_in_a_page, find_category, find_references
from merge import merge_chunks
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv)!=3:
	print len(sys.argv)
	print "Incorrect Format"
	exit()

PATH = "./"
FILENAME = sys.argv[1]

def write_to_chunk(doc_dict, file_name):
	with open(file_name, "w") as fl:
		for key in sorted(doc_dict):
			fl.write(str(key) + doc_dict[key] + "\n")

def update_page(page_dict, doc_dict, page_id):
	bt=""; tt=""; el=""; ct="" ; rf=""
	for key in page_dict:
		if page_dict[key][0] != 0:
			bt = str(page_dict[key][0]) #"b" +
		if page_dict[key][1] != 0:
			tt = str(page_dict[key][1]) #"t" +
		if page_dict[key][2] != 0:
			el = str(page_dict[key][2]) #"l" +
		if page_dict[key][3] != 0:
			ct = str(page_dict[key][3]) #"c" +
		if page_dict[key][4] != 0:
			rf = str(page_dict[key][4]) #"r" +
		if key not in doc_dict:
			doc_dict[key] = "," + str(page_id) + "." + bt + "." + tt + "." + el + "." + ct
		else:
			doc_dict[key] = doc_dict[key] + "," + str(page_id) + "." + bt + "." + tt + "." + el + "." + ct

path = os.path.join(PATH, FILENAME)
page_id = 0
totalCount = 0
in_revision = False
page_dict = {}
doc_dict = {}
chunk=0;
length_file = open("./index/length.txt", 'w')
lt_file = open("./index/lt.txt", "w")
link_title=""

for event, element in etree.iterparse(FILENAME, events=('start', 'end')):
	tname = strip_tag_name(element.tag)

	if event == "start":
		if tname == "page":
			main_text=""
			title=""
		if tname == "title":
			link_title=element.text
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
			totalCount+=1
			update_page(page_dict, doc_dict, page_id)
			if link_title is None:
				link_title=""
			lt_file.write(str(page_id)+":"+link_title+"\n")
			length_file.write(str(page_id)+":"+str(len(page_dict))+"\n")
			page_dict.clear();
			if(sys.getsizeof(doc_dict)>5242880):
				write_to_chunk(doc_dict, "./chunks/chunk"+str(chunk)+".txt")
				chunk+=1
				doc_dict.clear()

	element.clear()

merge_chunks(chunk, totalCount)



#dict_to_string(doc_dict)

#if __name__ == "__main__":
#    main()
