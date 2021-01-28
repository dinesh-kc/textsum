import nltk 
import re 
from nltk.corpus  import stopwords 
from nltk.tokenize import word_tokenize,sent_tokenize
import math 


# text = input("enter text")

## Pre-processing function 
'''
removes special characters from within a string 

parameters : s(str): Single input string 
return : stripped s(str): A string with special character removed.
'''
def remove_string_special_characters(s):
    #replace special character with ' '
    stripped = re.sub('[^\w\s]','',s)
    stripped = re.sub('_','',stripped)
    
    #changing any whitespace to one space 
    stripped = re.sub('\s+',' ',stripped)
    
    #removind start and end whitespace 
    stripped = stripped.strip()
    
    return stripped


def get_doc(text_sents_clean):
    '''
    input : text 
    output : splits the text into sentences & considers each sentence as a document , 
    calculates the total word count of each & returns document info
    '''
    doc_info = []
    i = 0
    for sent in text_sents_clean:
#         print(sent)
        i += 1
        count = count_words(sent)
        temp = {'doc_id':i,'doc_length':count}
        doc_info.append(temp)
    return doc_info

## count word function 
def count_words(sent):
    '''
    input : word 
    returns : total no. of words in the sentence
    '''
    count = 0
    words = word_tokenize(sent) ##  Tokenizes the word NLP library
    for word in words:
        count += 1
    return count
## creating frequency dictionary in for each word in a document 

def create_freq_dict(sents):
    '''returns frequency dictionary of each words '''
    i = 0
    freqDict_list = []
    for sent in sents:
        i += 1 
        freq_dict = {}
        words = word_tokenize(sent) ### NLP library
        for word in words:
            word  = word.lower()
            if word in freq_dict:
                freq_dict[word] += 1 
            else:
                freq_dict[word] = 1 
            temp = {'doc_id':i,'freq_dict':freq_dict}
        freqDict_list.append(temp)
    return freqDict_list
# computing TF 
def computeTF(doc_info,freqDict_list):
    '''
    tf = (frequency of the term in the doc /total no of terms in the doc )
    '''
    TF_scores = []
    for tempDict in freqDict_list:
        id = tempDict['doc_id']
        for k in tempDict['freq_dict']:
            temp = {
                'doc_id':id,
                'TF_score':tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                'key':k
            }
            TF_scores.append(temp)
    return TF_scores

## Computing IDF 
def computeIDF(doc_info,freqDict_list):
    '''
    idf = ln(total no of docs /number of docs with term in it )
    '''
    IDF_scores = []
    counter = 0
    for dict in freqDict_list:
        counter += 1
        for k in dict['freq_dict'].keys():
            count = sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp = {'doc_id':counter,'IDF_score':math.log(len(doc_info)/count),'key':k}
            IDF_scores.append(temp)
            
    return IDF_scores

def computeTFIDF(TF_scores,IDF_scores):
    TFIDF_scores = []
    for j in IDF_scores:
        for i in TF_scores:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id':j['doc_id'],
                       'TFIDF_score':j['IDF_score']*i['TF_score'],
                        'key':i['key']
                       }
        TFIDF_scores.append(temp)
        
    return TFIDF_scores


def get_summary(sentence_info):
    sum = 0 
    summary = []
    array = []
    for temp_dict in sentence_info:
        '''
        this gets sum of scores of all sentences 
        '''
        sum += temp_dict['sent_score']
    avg = sum/len(sentence_info) # computing the average of TFIDF
    for temp_dict in sentence_info:
        '''
        gets sentence score and stores them in array 
        '''
        array.append(temp_dict['sent_score'])
#     stdev =  statistics.stdev(array) ## computing the standard deviation on the array 
    new_summary = ''
    for sent in sentence_info:
        '''
        getting the summary 
        '''
        if (sent['sent_score']) >= avg: # +1.5*stdev
            summary.append(sent['sentence'])
        new_summary  = '\n'.join(summary)
    return new_summary


def get_sent_score(TFIDF_scores,text_sents,doc_info):
    '''
    doc-info = word count of each document 
    text_sents = tokenized document 
    prints our summary & returns out scores of each sentence in a list. 
    
    score of sentence is calculated by adding the TFIDF scores of the words that make up the sentence .
    '''
    sentence_info = []
    for doc in doc_info:
        '''
        loops through each document(sentence ) and calculates their 'sent_score'
        '''
        sent_score = 0
        for i in range(0,len(TFIDF_scores)):
#             print(TFIDF_scores[i])
            temp_dict = TFIDF_scores[i]
            if doc['doc_id'] == temp_dict['doc_id']:
                sent_score += temp_dict['TFIDF_score']
            temp = {
                'doc_id':doc['doc_id'],
                'sent_score':sent_score,
                'sentence':text_sents[doc['doc_id']-1]
                
            }
        sentence_info.append(temp)
    return sentence_info
    


class fetch_summary(object):
    def __init__(self,text):
        self.text_sents = sent_tokenize(text)

        print("### tokenized sentences ###")
        print(self.text_sents)


        print("removes the special characters ")
        self.text_sents_clean = [remove_string_special_characters(s) for s in self.text_sents] 
        print(self.text_sents_clean)

        print('\n\n\n')
        print("#############")
        print("Documents ")
        self.doc_info  = get_doc(self.text_sents_clean)
        print(self.doc_info)

        print('\n\n\n')
        print("#############")
        print("frequency dict ")
        self.freqDict_list = create_freq_dict(self.text_sents_clean)
        print(self.freqDict_list)


        print('\n\n\n')
        print("#############")
        print("TF value")

        self.TF_scores = computeTF(self.doc_info,self.freqDict_list)
        print(self.TF_scores)


        print('\n\n\n')
        print("#############")
        print("IDF value")
        self.IDF_scores = computeIDF(self.doc_info,self.freqDict_list)
        print(self.IDF_scores) ## calculating the idf 


        print('\n\n\n')
        print("#############")
        print("TFIDF value")
        self.TFIDF_scores = computeTFIDF(self.TF_scores,self.IDF_scores)
        print(self.TFIDF_scores)

        print('\n\n\n')
        print("#############")
        print("Sentence Scoring ")
        self.sentence_info = get_sent_score(self.TFIDF_scores,self.text_sents,self.doc_info) # returns sentence scoring 
        print(self.sentence_info)

        summ = get_summary(self.sentence_info)
        print('\n\n\n')
        print("#############")
        print("Final Summary ")
        print(summ)




 

    def load_summary(self,text):
        summ = get_summary(self.sentence_info)
        return summ
        # print('\n\n\n')
        # print("#############")
        # print("Final Summary ")
        # print(summ)

     