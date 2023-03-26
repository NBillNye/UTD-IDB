from keybert import KeyBERT
import pickle

def load():
    with open('KeyBERT_model.pickle', 'rb') as f:
        kw_model = pickle.load(f)
        return kw_model

def extract_keywords(kw_model, document: str, ngram_range=3, top_n=10) -> list:
    keywords = kw_model.extract_keywords(document,
                                         keyphrase_ngram_range=(1,ngram_range),
                                         stop_words='english',
                                         highlight=False,
                                         top_n=top_n)
    
    keywords = list(dict(keywords).keys())    

    return keywords

if __name__ == '__main__':
    with open('KeyBERT_model.pickle', 'wb') as f:
        kw_model = KeyBERT(model='all-mpnet-base-v2')
        pickle.dump(kw_model, f)

    
    
    