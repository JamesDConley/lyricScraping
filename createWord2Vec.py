import csv
from gensim.models import Word2Vec
import pickle
import multiprocessing

def pickleSave(filename,  object):
    pickleOut = open(filename,  'wb')
    pickle.dump(object,  pickleOut)
    pickleOut.close()

def removeNonAlpha(text):
    return ''.join(letter for letter in text if letter.isalpha() or letter == " ")

#Reading in the raw data
lyricFile = open('lyrics.csv')      
csv_reader = csv.reader(lyricFile,  delimiter=',')

#Setting these here will make it easier to use this code on similar datasets
lyricColumn = 5
genreColumn = 4

lines = []

#Sentences will be lines of songs
for row in csv_reader:
    for line in row[lyricColumn].split("\n"):
        words = removeNonAlpha(line).split(" ")
        lines.append(words)

num_workers = multiprocessing.cpu_count()

w2v = Word2Vec(sg=1,  seed = 1,  size=300, window=7,sample = 1e-3,  min_count=3, workers=num_workers)
w2v.build_vocab(lines)
#print(len(w2v.vocab))
w2v.train(lines,  total_examples = w2v.corpus_count,  epochs = 10)
pickleSave("w2v.pickle", w2v)

print(w2v.wv['love'])