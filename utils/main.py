from algo import *
# text = input("Enter TExt")


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
        print('\n\n\n')
        print("#############")
        print("Final Summary ")
        print(summ)

        



if __name__ == '__main__':
    # text = input("enter text  ")
    text = '''
        Nepal, the landlocked multiethnic, multilingual, multi-religious country, is situated north of India in the Himalayas, in the region where, about 40 to 50 million years ago, the Indian subcontinent has crashed into Asia. Because of that accident, Nepal has some of the world's highest mountains including Sagarmatha (Mt. Everest, 8848m, which it shares with Tibet (by now a province of China). The highest mountain on Earth is towering above populated valleys and forested plains.
        Somewhere here in the Kapilavastu district, there is a place called Lumbini where in about 500 B.C.E. Queen Mayadevi is said to have given birth to Siddhartha Gautama, better known as Buddha.

        Nepal can be divided broadly into three ecological zones: the lowland, the midland and the highland.
        The altitude of the Himalayan Region (the highland) ranges between 4877 m - 8848 m, It includes 8 of the highest 14 summits in the world, which exceed altitude of 8000 meters including Mount Everest.

        The mountain region accounts for about 64 percent of total land area, which is formed by the Mahabharat range that soars up to 4877 m and the lower Churia range.
        The lowland Terai, the flat river plain of the Ganges with a belt of marshy grasslands, savannas, and forests, occupies about 17 percent of the total land area of the country.
    '''
    fetch_summary(text)



# def fetch_summary(text):
  

    