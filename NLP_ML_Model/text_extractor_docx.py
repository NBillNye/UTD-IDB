import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from docx import Document
import pickle
import os

import keyword_extraction
import pipeline

class Doc:
    def __init__(self, text, keywords):
        self.text = text
        self.keywords = keywords


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
    
    error_threshold = 0.5 # similarity score threshold; subject to change
    
    print(f'matching func|| query: {query} , documents: {documents}')
    
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
    
def extract_text_from_tables(docx_path: str) -> list:
    '''
    extract text from tables in a docx by row
    everything within the same row is put into the same document
    '''
    #print('Extracting text from tables...')
    
    docx = Document(docx_path)
    table_documents = []
    for table in docx.tables:
        for row in table.rows:
            row_content = ''
            for cell in row.cells:
                row_content += cell.text + ' '
            table_documents.append(row_content)
    
    #print('Done extracting text from tables.')
    
    return table_documents
    
def extract_text_from_bold(docx_path: str) -> list:
    '''
    extract text using the position of bolded text
    everything after the bolded text is added to the same document
    until the next bolded text
    '''
    docx = Document(docx_path)
    bolded_documents = []
    
    counter = 0
    for paragraph in docx.paragraphs:
        for run in paragraph.runs:
            if run.bold:
                bolded_documents.append(run.text)
                counter += 1
            elif counter == 0: # whenever the docx starts with a non-bold run
                bolded_documents.append(run.text)
            else:
                bolded_documents[counter] += run.text
    
    return bolded_documents  

# TENTATIVE
# How and where we save the keywords of a document may change (i.e. in database instead)
def process_syllabus(docx_path, kw_model):
    '''
    Pull text in tables and organize them into a list of 'documents'
    for each document, determine keywords for each document and save them
    to a class containing both the text and keywords
    finally, pickle a list of these syllabus document classes for later use
    '''
    #print('Processing syllabus...')
    
    table_documents = extract_text_from_tables(docx_path)
    
    docs = []
    for document in table_documents:
        keywords = keyword_extraction.extract_keywords(kw_model, document, ngram_range=3, top_n=10)
        #print(keywords)
        docs.append(Doc(document, keywords))
    
    with open('syllabus_docs.pickle', 'wb') as f:
        pickle.dump(docs, f)
    
    #print('Done processing syllabus.')

# not really sure if we need this tbh
def get_similar_words(keyword):
    similar_words = []
    
    for syn in wordnet.synsets(keyword):
        for synonym in syn.lemmas():
            similar_words.append(synonym.name())
    print(f'Similar words: {set(similar_words)}')

if __name__ == '__main__':
    docx_path = 'Syllabus-3377-converted.docx'
    query = 'what is the grading policy?' # input query
    
    kw_model = keyword_extraction.load()
    
    # only process once
    if not os.path.exists('syllabus_docs.pickle'):
        process_syllabus(docx_path, kw_model)
    
    with open('syllabus_docs.pickle', 'rb') as f:
        all_docs = pickle.load(f)
        
        # only retrieve the documents that contain the keywords
        only_key_docs = []
        query_keywords = keyword_extraction.extract_keywords(kw_model, query, ngram_range=2, top_n=3)
        for doc in all_docs:
            for keyword in query_keywords:
                doc_keywords = ' '.join(doc.keywords)
                if keyword in doc_keywords:
                    only_key_docs.append(doc_keywords)
                    print(f'Added doc keywords: {doc_keywords}')

    # map keywords to documents
    doc_dict = {}
    for doc in all_docs:
        doc_dict[' '.join(doc.keywords)] = doc.text
    
    matches = get_matching_documents(' '.join(query_keywords), only_key_docs)
    # output top 5 matches
    for i, match in enumerate(matches[:5]):
        print(str(i) + ': ' + doc_dict[match] + '\n')
    
