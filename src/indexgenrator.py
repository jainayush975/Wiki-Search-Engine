import os,time,csv
import codecs
import re
import xml.etree.ElementTree as etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PATH = "./"
FILENAME = 'hiwiki-20170801-pages-meta-current.xml'
ENCODING = "utf-8"

# Used to strip the namespace from the tags.
def strip_tag_name(t):
    t = element.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

path = os.path.join(PATH, FILENAME)

totalCount = 0
file_words = {}
all_words = {}

