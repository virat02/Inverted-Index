import pickle

stop_list = []                                      #list of stop lists

tf = []                                             #list of term frequencies

t_tf_df = {}                                        #dictionary containing the term as a key and the values as a list of
                                                    #term frequency of the term in the whole corpus and the document frequency of the term

with open("inverted_list_encoded.txt", 'rb') as f:
    t1 = pickle.loads(f.read())

with open("task3_part1_unigram_unsorted_encoded.txt", 'rb') as f:
    t_tf = pickle.loads(f.read())

with open("task3_part2_unigram-encoded.txt", 'rb') as f:
    t_dID_df = pickle.loads(f.read())

t = t1.keys()
tf = list(t_tf.values())
dID_df = list(t_dID_df.values())
df = []

for i in range (0, len(dID_df)):
    df.append(dID_df[i][1])
    
i = 0

for term in t:
    tuple = tf[i] , df[i]
    t_tf_df[term] = tuple
    i += 1

for term in t_tf_df:
    if (t_tf_df[term][0] > 5000 and t_dID_df[term][1] > 675):
        stop_list.append(term)

f = open('StopList.txt' , 'w')
for i in range (0,len(stop_list)):
    f.write(stop_list[i]+"\n")
f.write("\nTotal Number of Stop List words: %d" %len(stop_list))
f.close()
