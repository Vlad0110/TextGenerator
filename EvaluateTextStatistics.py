import collections
import sys
import os
try:
   import cPickle as pickle
except:
   import pickle

def get_text(directory, file_name):
    with open(directory + "/" + file_name, 'r') as fl:
        clean_text = fl.read()
    return clean_text
    
def count_bigrams(words):
    bigrams = dict()
    
    for pair in zip(words, words[1:]):
        if (not pair[0] in bigrams):
            bigrams[pair[0]] = collections.Counter()
        bigrams[pair[0]][pair[1]] += 1
        
    return bigrams
    
def update_bigram_counter(bigrams_counter, words):
    cur_bigrams = count_bigrams(words)    
    for word in cur_bigrams:
        if word in bigrams_counter:
            bigrams_counter[word].update(cur_bigrams[word])
        else:
            bigrams_counter[word] = cur_bigrams[word]
    return bigrams_counter
    
def remove_rare_words(words_counter):
    MIN_WORDS_COUNT = 7
    result = collections.Counter()
    for word in words_counter:
        if (words_counter[word] >= MIN_WORDS_COUNT):
            result[word] = words_counter[word]
    return result

def remove_rare_bigrams(bigrams_counter, result_words_counter):
    MIN_BIGRAMS_COUNT = 2
    result = dict()
    for word in bigrams_counter:
        if (not word in result_words_counter):
            continue    
        word_result = collections.Counter()
        for second_word in bigrams_counter[word]:
            if (second_word in result_words_counter and 
                bigrams_counter[word][second_word] >= MIN_BIGRAMS_COUNT):
                    
                word_result[second_word] = bigrams_counter[word][second_word]
                
        if (not word_result):
            word_result['.'] = 1
        result[word] = word_result
            
    return result
    
def save_statistics(result_words_counter, result_bigrams_counter):
    with open("words_counter.txt", 'w') as fl:
        pickle.dump(result_words_counter, fl)
        
    with open("bigrams_counter.txt", 'w') as fl:
        pickle.dump(result_bigrams_counter, fl)
  
  
if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    directory = sys.argv[1]
else:
    print("Please, enter clean corpus directory:")
    directory = raw_input()
    
words_counter = collections.Counter()
bigrams_counter = dict()

file_names = os.listdir(directory)

for name in file_names:
    try:
        clean_text = get_text(directory, name)
    except:
        print "\nCan't process {}, so skip it".format(name)
        os.remove(directory + "/" + name)
        continue
        
    words = clean_text.split()
    words_counter.update(collections.Counter(words))
    bigrams_counter = update_bigram_counter(bigrams_counter, words)
    
result_words_counter = remove_rare_words(words_counter)
result_bigrams_counter = remove_rare_bigrams(bigrams_counter, result_words_counter)
save_statistics(result_words_counter, result_bigrams_counter)
        