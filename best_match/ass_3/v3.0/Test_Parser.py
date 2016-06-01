#!/usr/bin/python

from Parser import read_wibbi
import os

def printInvertedDB(inverted_db, output):
    
    toPrint = ""
    for term in inverted_db.keys():
        toPrint = term + " "
        for doc in inverted_db[term]:
            toPrint += doc + ","
            toPrint+=str(inverted_db[term][doc])+";"
        print >> output, toPrint
        
def invert(db):
    inverted_db = dict()
    for url in db.keys():
        size = len(db[url])
        for word in db[url]:
            if word not in inverted_db.keys():
                inverted_db[word] = dict()
            count = db[url].count(word)
            inverted_db[word][url] = float(count)/ size
    return inverted_db

def set_default(obj):
	if isinstance(obj,set):
		return list(obj)
	raise TypeError

def create_link(dataset):
  for name1 in dataset:
      for name2 in dataset:
         if name1!=name2:

             U = random.sample(dataset[name1]["graph"].keys(),10)
             V = random.sample(dataset[name2]["graph"].keys(),10)

             for i in range(len(U)):
                 if V[i] not in dataset[name1]["graph"][U[i]]: 
                     dataset[name1]["graph"][U[i]].add(V[i])

"""
def invert_db(dataset):
  new_db = dict()
  temp_db = dict()
  for name in dataset:
    db = dataset[name]["db"]
    
    for k in db:
      len_k = len(db[k])
      
      for w in db[k]:
        if w not in temp_db:
          temp_db[w]=dict()
        count = db[k].count(w)
        temp_db[w][k] = float(count)/len_k
  
  for w in temp_db:
    sorted_docs = OrderedDict(sorted(temp_db[w].items(), key=operator.itemgetter(1), reverse=True))
    new_db[w] = sorted_docs
  dataset["inv_db"] = new_db
"""


dataset = dict()
for filename in os.listdir(os.getcwd()+"/dataset/"):
    
    if filename.endswith(".pages"):
        print("Parsing: " + filename)
        graph,db = read_wibbi(filename)
        dataset[filename] = db
        print("----------------")
print("------FINISHED PARSING-----")

print ("------STARTING INVERSE----------")
output = open("inverted_db.txt","w")
for filename in dataset.keys():
    print("-------INVERTING "+filename+ "-------------")
    printInvertedDB(invert(dataset[filename]), output)
output.close()

print("------DONE-----")