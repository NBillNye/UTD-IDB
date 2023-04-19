import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import pickle
import os

import keyword_extraction
from pipeline import *
import time

class Doc:
    def __init__(self, text: str, keywords: list, origin: str | int):
        self.text = text # full text of one theme
        self.keywords = keywords # words that highlight the document's theme
        self.origin = origin # any course material: str | thread ID: int
        
    def __init__(self):
        return
        
    def set_text(self, text: str):
        self.text = text
    
    def set_keywords(self, keywords: list):
        self.keywords = keywords
        
    def set_origin(self, origin: str | int):
        self.origin = origin
        if type(origin) is str:
            self.type = 'file'
        else:
            self.type =  'thread'

# getter and setter for inputs
class Inputs:
    def __init__(self, class_ID: int , query: str):
        self.class_ID = class_ID
        self.query = query

    def __init__(self):
        return

    def set_class_ID(self, class_ID):
        self.class_ID = class_ID

    def set_query(self, query):
        self.query = query
        
    def get_query_keywords(self):
        kw_model = keyword_extraction.load()
        
        return keyword_extraction.extract_keywords(kw_model, self.query, ngram_range=2, top_n=3) #TENTATIVE ARGS
        
        

stopwords = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_lg') # py -m spacy download en_core_web_lg
lemmatizer = WordNetLemmatizer()

def preprocess_text(text: str) -> str:
    ''' 
    remove extra spaces, newlines, tabs, stopwords, numbers
    we will end up with a list of unique and significant words
    '''
    text = nltk.re.sub(r'\s+', ' ', text).strip()
    text = text.replace('\n', '').replace('\t', '')
    text = word_tokenize(text)
    text = [lemmatizer.lemmatize(word.lower()) for word in text if word not in stopwords and word.isalpha()]
    text = set(text)

    #print(text)
    #return a single text string
    return ' '.join(list(text))

# use spacy to compute similarity between query and each document
def get_matching_documents(query: str, documents: list) -> list:
    #print('Calculating similarities...')
    
    error_threshold = 0.5 # similarity score threshold; TENTATIVE
    
    #print(f'matching func|| query: {query} , documents: {documents}')
    
    query = nlp(preprocess_text(query))
    nlp_docs = []
    for document in documents:
        nlp_docs.append(nlp(preprocess_text(document)))
    
    similarity_scores = [query_similarity := query.similarity(doc) for doc in nlp_docs]
    # print(similarity_scores)
    
    # map documents to their similarities
    doc_similarity_tuples = []
    for i, doc in enumerate(documents):
        doc_similarity_tuples.append((doc, similarity_scores[i]))
    
    # descending sort
    sorted_docs_by_score = sorted(doc_similarity_tuples, key=lambda x:x[1], reverse=True)
    # print(sorted_docs_by_score)
    
    document_matches = []
    for doc, score in sorted_docs_by_score:
        if score > error_threshold:
            if doc not in document_matches:
                # match found
                print(f'Score: {score}')
                document_matches.append(doc)
    #print('Done calculating similarities.')
    
    return document_matches

def get_similar_Docs(docs: list[Doc], query_keywords: list[str], top_n: int):
    
    doc_origin_dict = {}
    for doc in docs:
        doc_origin_dict[' '.join(doc.keywords)] = doc

    doc_keywords = [' '.join(doc.keywords) for doc in docs]

    # get similarities for files
    matches = get_matching_documents(' '.join(query_keywords), doc_keywords)
    
    top_results = []
    for match in matches[:min(top_n,len(matches))]:
        result = doc_origin_dict[match]
        top_results.append(result.origin)
    
    return top_results

#Takes in query and class ID and retrieves similar course material file paths and thread IDs
def query_model_detailed(new_query: Inputs):
    
    start = time.time_ns()

    query_keywords = new_query.get_query_keywords()
   
    # get processed documents list corresponding to class ID
    class_processed_documents_path = 'class_data/' + str(new_query.class_ID) + '.pickle' # TENTATIVE
    try: 
        if os.stat(class_processed_documents_path).st_size > 0:
            with open(class_processed_documents_path, 'rb') as file:
                # list of processed Doc objects of one class
                processed_documents = pickle.load(file)
    except OSError:
        print(f'No existing file for processed documents in with class ID {new_query.class_ID}')
        return [], []
    
    # loop through and find relevant documents
    # organize into two lists: course material file paths + thread IDs
    file_Docs = []
    thread_Docs = []
    for document in processed_documents:
        doc_keywords = ' '.join(document.keywords)
        for kw in query_keywords:
            if kw in doc_keywords:
                if document.type == 'file' and document not in file_Docs:
                    print('Matching file-type document found')
                    file_Docs.append(document)
                elif document not in thread_Docs:
                    print('Matching thread-type document found')
                    thread_Docs.append(document)
    
    # get similarities for files
    res_file_list = []
    res_thread_list = []

    if len(file_Docs) > 0:
        res_file_list = get_similar_Docs(file_Docs, query_keywords, top_n=3)
    # get similarities for threads
    if len(thread_Docs) > 0:
        res_thread_list = get_similar_Docs(thread_Docs, query_keywords, top_n=3)
    
    end = time.time_ns()
    delta = round((end-start)/1000000, 2)
    print(f'query time: {delta} ms')

    return res_thread_list, res_file_list
    
    
#Takes in query and class ID and retrieves similar course material file paths and thread IDs
def query_model(class_ID: int, query: str):
    new_query = Inputs()
    new_query.set_class_ID(class_ID)
    new_query.set_query(query)

    return query_model_detailed(new_query)
    
# update_

if __name__ == '__main__':
    threads, files = query_model(12345, 'What is the grading policy?')

    print(f'threads match: {threads}')
    print(f'files match: {files}')