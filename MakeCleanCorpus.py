import sys
import os
import re

def get_text(directory, file_name):
    with open(directory + "/" + file_name, 'r') as fl:
        text = fl.read()
    return text

def make_clean_text(text):
    regex = re.compile('[^a-z?.!]')
    clean_text = regex.sub(' ', text.lower())
    clean_text = clean_text.replace('.', ' . ')
    clean_text = clean_text.replace('?', ' . ').replace('!', ' . ')
    return clean_text

def save_clean_text(name, clean_text):
    with open("clean_corpus/" + name, 'w') as fl:
        fl.write(clean_text)

if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    directory = sys.argv[1]
else:
    print("Please, enter corpus directory:")
    directory = raw_input()
    
file_names = os.listdir(directory)

for name in file_names:
        try:
            text = get_text(directory, name)
        except:
            print "\nCan't process {}, so skip it".format(name)
            os.remove(directory + "/" + name)
            continue
        
        clean_text = make_clean_text(text)
        save_clean_text(name, clean_text)