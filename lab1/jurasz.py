__author__ = 'wiktor'

import os
import sys
import re
import codecs

def print_groups_as_list(groups):
    for i in xrange(0, len(groups)):
        if(len(groups[i]) > 0):
            print(groups[i] + ","),
    print

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    meta_pattern_prefix = "(?:\\n*"
    meta_pattern_infix = ".*CONTENT=\")"
    meta_pattern_actuall_content = "(.*)"
    meta_pattern_sufix = "(?:\".*).*"

    # finding author
    find_author_pattern = meta_pattern_prefix + "\"AUTOR\"" + meta_pattern_infix + meta_pattern_actuall_content + meta_pattern_sufix
    author = re.search(find_author_pattern, content).group(1)

    # finding section
    find_section_pattern = meta_pattern_prefix + "\"DZIAL\"" + meta_pattern_infix + meta_pattern_actuall_content + meta_pattern_sufix
    section = re.search(find_section_pattern, content).group(1)

    # finding key words
    find_keyWord_pattern = meta_pattern_prefix + "\"KLUCZOWE" + meta_pattern_infix + meta_pattern_actuall_content + meta_pattern_sufix
    key_words_groups = re.findall(find_keyWord_pattern, content)

    # finding section to look for other calues
    find_text_section_pattern  = "(?:.*?<P>)(.*?<META)(?:.*)"
    complied_patter = re.compile(find_text_section_pattern, re.S)
    text_section = re.search(complied_patter , content).group(1)

    # finding shortcuts
    short_cuts = re.findall(r'\s+[a-zA-Z]{2,3}\.', text_section)

    # finding integers
    integers_tuples = re.findall(r'(\s+|[\s+-])(0|[1-9]\d{0,3}|[1-2]\d{1,4}|31\d{1,3}|32[0-6]\d{1,2}|327[0-5]\d|3276[0-7])\s+', text_section)
    integers = []
    for i in integers_tuples:
        integers.append(''.join(i))

    # finding integers
    real_tuples = re.findall(r'(\s+|[\s+-])(\d+\.\d+|\d+\.|\.\d+|\d+\.\d+e\+\d+)\s', text_section)
    real = []
    for i in real_tuples:
        real.append(''.join(i))

    # finding dates
    dates_tuples = re.findall('[^0-9]((?:\d{4}(?P<delimiter1>[-/.]))'
                              '(?:(?:[0-2][0-9]|3[01])(?P=delimiter1)(?:0[13578]|1[02]))|'
                              '(?:(?:[0-2][0-9]|30)(?P=delimiter1)(?:0[469]|11))|'
                              '(?:[0-2][0-9](?P=delimiter1)02))|'

                              '((?:(?:(?:[0-2][0-9]|3[01])(?P<delimiter2>[-/.])(?:0[13578]|1[02]))|'
                              '(?:(?:[0-2][0-9]|30)(?P<delimiter3>[-/.])(?:0[469]|11))|'
                              '(?:[0-2][0-9](?P<delimiter4>[-/.])02))'
                              '(?:(?P=delimiter3)\d{4}|(?P=delimiter2)\d{4}|(?P=delimiter4)\d{4}))[^0-9]]',
                      text_section)

    # finding emails
    emails = re.findall(r'(\b\w+@(\w+\.\)+\w+))', text_section)

    # finding sentences
    sentences = re.findall(r'([A-Z].{4,}?[\.!\?\n]+)(?=(?:\s+[A-Z][^\.]{3,}|\s*<))', text_section)
    fp.close()
    print("nazwa pliku:" + str(filepath))
    print("autor: " + author)
    print("dzial: " + section)
    print("slowa kluczowe: "),
    print_groups_as_list(key_words_groups)
    print("liczba zdan: " + str(len(sentences)))
    print("liczba skrotow: " + str(len(set(short_cuts))))
    print("liczba liczb calkowitych z zakresu int: " + str(len(set(integers))))
    print("liczba liczb zmiennoprzecinkowych: " + str(len(set(real))))
    print("liczba dat: " + str(len((dates_tuples))))
    print("liczba adresow email: " + str(len(set(emails))))
    print("\n")



try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)

