import pickle

d2 = {}                                                 #dictionary to store term, term frequency
docID = 0												#gives the document ID for a particular document

url_crawled = []
with open('urlsCrawledBFS.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
url_crawled.extend(l)

def generate_ngrams(words_list, n):						#Function to generate n-grams
    ngrams_list = []

    for num in range(0, len(words_list)):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)

    return ngrams_list

def inverted_index(url):								#Function to generate inverted index
    inv_index_bigram = {}
    global docID
    docID += 1
    filename = url.split('https://en.wikipedia.org/wiki/')[1]
    newfilename = filename + 'inv_index.txt'
    filename = filename + '.txt'
    f = open(filename ,'r', encoding = 'utf-8')
    terms = f.read()
    term_list = terms.split()
    bigrams = generate_ngrams(term_list, 2)
    for term in bigrams:
        if terms.count(term) == 0:
            continue
        else:
            d2[term] = terms.count(term)
        tuple = docID , d2[term]
        inv_index_bigram[term] = tuple
        #print(t," -> (",docID,",",d[t],")")

    return inv_index_bigram

parent_inverted_list = {}
for link in url_crawled:
    child_inverted_list = inverted_index(link)
    for term in child_inverted_list:

        if term in parent_inverted_list:

            parent_inverted_list[term].append(child_inverted_list[term])     #append the (docID,tf) for the term if the same term appears in another document

        else:

            parent_inverted_list[term] = [child_inverted_list[term]]

output = open('inverted_list_bigram.txt', 'w+', encoding = 'utf-8')
for term in parent_inverted_list:
    output.write("%s -> %s\n" %(term , parent_inverted_list[term]))
output.close()

output = open('inverted_list_bigram_encoded.txt', 'wb')
pickle.dump(parent_inverted_list , output)
output.close()
