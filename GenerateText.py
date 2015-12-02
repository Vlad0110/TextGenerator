import collections
import random
try:
   import cPickle as pickle
except:
   import pickle
   

class TextGenerator(object):
    PARAGRAPH_PROPABILITY = 0.18
    
    def __init__(self, first_name, second_name):
        with open(first_name, 'r') as fl: 
            self.words_counter = pickle.load(fl)
            
        with open(second_name, 'r') as fl:
            self.bigrams_counter = pickle.load(fl)
            
    def generate_word(self, words):
        words_total_number = sum(words.values())
        word_number = random.randint(0, words_total_number - 1)
        cur_sum = 0
        for word in words:
            cur_sum += words[word]
            if cur_sum >= word_number:
                return word
            
    def generate_sentence(self):
        next_word = self.generate_word(self.words_counter)
        sentence = []
        
        while(next_word != '.'):
            prev_word = next_word
            sentence.append(prev_word)
            next_word = self.generate_word(self.bigrams_counter[prev_word])
            
        if (len(sentence) < 2):
            return self.generate_sentence()
            
        sentence = ' '.join(sentence)
        sentence = sentence[0].upper() + sentence[1:]
        if random.random() < self.PARAGRAPH_PROPABILITY:
            next_word = '.\n\t'
        else:
            next_word = '. '
        return sentence + next_word
            
    def generate_text(self, number_of_sentences):
        text = '\t'
        for iterator in xrange(number_of_sentences):
            text += self.generate_sentence()
        return text
           
    
NUMBER_OF_SENTENCES = 1000
first_fl = "words_counter.txt"
second_fl = "bigrams_counter.txt"

text_generator = TextGenerator(first_fl, second_fl)
generated_text = text_generator.generate_text(NUMBER_OF_SENTENCES)

with open("GeneratedText.txt", 'w') as fl:
    fl.write(generated_text)