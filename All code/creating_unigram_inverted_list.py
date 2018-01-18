import pickle
import collections

d1 = {}                                                      #dictionary to store term, term frequency 
docID = 0                                                    #gives the document ID for a particular document
doc_name = []                                                #list to store all the document names obtained
docID_doclen = {}                                            #dictionary to store the document length of a particular document
docID_docName = {}

url_crawled = []
with open('urlsCrawledBFS.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
url_crawled.extend(l)

def generate_ngrams(words_list, n):                           #Function to generate n-grams
    ngrams_list = []

    for num in range(0, len(words_list)):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)

    return ngrams_list

def inverted_index(url):                                     #Function to generate inverted index
    inv_index_unigram = {}
    global docID, doc_name
    docID += 1
    filename = url.split('https://en.wikipedia.org/wiki/')[1]
    doc_name.append(filename)
	docID_docName[docID] = doc_name
    filename = filename + '.txt'
    f = open(filename ,'r', encoding = 'utf-8')
    terms = f.read()
    term_list = terms.split()
    docID_doclen[docID] = len(term_list)
    for term in term_list:
        if terms.count(term) == 0:
            continue
        else:
            d1[term] = terms.count(term)
        tuple = docID , d1[term]
        inv_index_unigram[term] = tuple

    return inv_index_unigram

parent_inverted_list = {}
for link in url_crawled:
    child_inverted_list = inverted_index(link)
    for term in child_inverted_list:

        if term in parent_inverted_list:

            parent_inverted_list[term].append(child_inverted_list[term])              #append the (docID,tf) for the term if the same term appears in another document

        else:

            parent_inverted_list[term] = [child_inverted_list[term]]

inv_list_unigram = collections.OrderedDict(sorted(parent_inverted_list.items()))      #sort the inverted index

output = open('inverted_list_unigram.txt', 'w+', encoding = 'utf-8')
for term in inv_list_unigram:
    output.write("%s -> %s\n" %(term , inv_list_unigram[term]))
output.close()

output = open('inverted_list_unigram_encoded.txt' , 'wb')
pickle.dump(inv_list_unigram , output)
output.close()

#File to show document ID to document Name mapping

f = open("DocumentIDs.txt", 'w', encoding = 'utf-8')
for i in range (0,1000):
    f.write("Document ID : %d Document Name : " %(i+1))
    f.write(doc_name[i] + "\n")
f.close()

f = open("DocumentID-DocLen.txt", 'w', encoding = 'utf-8')
f.write(str(docID_doclen))
f.close()

output = open("DocumentID_DocName_encoded.txt" , 'wb')
pickle.dump(docID_docName , output)
output.close()

output = open('DocumentID-DocLen-encoded.txt' , 'wb')
pickle.dump(docID_doclen , output)
output.close()

