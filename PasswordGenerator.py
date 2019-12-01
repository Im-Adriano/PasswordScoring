import tensorflow as tf
import math
import numpy as np
import random
import GenGoodPass

class PASSWORD_GENERATOR(tf.keras.utils.Sequence):
    def __init__(self, batchsize):
        self.batch_size = batchsize
        self.charset_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.charset_special = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '-', '?', '.']
        self.words = self.load_words()
        self.badPasswords = self.load_rockyou()

    def load_words(self):
        with open('top.txt', 'r') as f:
            words = f.read().split()    
        return words
    
    def load_rockyou(self):
        passwords = []
        with open('rockyou.txt', 'r', encoding='latin-1') as f:
            passwords = f.read().split()  
        temp = []  
        for password in passwords:
            if len(password) < 30:
                temp.append(password)
        return temp

    def char_to_num(self, char):
        return ord(char)

    def num_to_chr(self, num):
        return chr(num)
    
    def gen_pass(self, score):
        charset = self.charset_numbers
        joinStr = ''
        if score == 0:
            return self.badPasswords[random.randint(0,len(self.badPasswords)-1)], str(0)
        if random.random() > .5:
            return GenGoodPass.generatePassword(self.words, len(self.words))
        else:
            if(score > 2):
                charset += self.charset_special
            if score > 3:
                joinStr = charset[random.randint(0,len(charset)-1)] 
            return (joinStr.join([self.words[random.randint(0,len(self.words)-1)].title() for _ in range(score)]) +
                ''.join([charset[random.randint(0,len(charset)-1)] for _ in range(score+1)]), str(score))
            
    def __len__(self):
        return int(math.floor(len(self.badPasswords)*4/self.batch_size))

    def __getitem__(self, idx):
        sequences = []
        labels = []
        for i in range(idx, idx+self.batch_size):
            seq, lab = self.gen_pass(random.randint(0,4))
            text_as_int = np.fromiter((self.char_to_num(c) for c in seq), dtype=np.int)
            text_as_int = np.pad(text_as_int, (0,70-len(text_as_int)))
            sequences.append(text_as_int)
            label = np.zeros(5)
            label[int(lab)] = 1
            labels.append(label)
        
        return np.array(sequences), np.array(labels)

