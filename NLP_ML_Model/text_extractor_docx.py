import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from docx import Document


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
    error_threshold = 0.5 # similarity score threshold; subject to change
    
    print(query)
    
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
            # match found
            document_matches.append(doc)
            
    return document_matches
    
def extract_text_from_tables(docx_path: str) -> list:
    '''
    extract text from tables in a docx by row
    everything within the same row is put into the same document
    '''
    
    docx = Document(docx_path)
    table_documents = []
    for table in docx.tables:
        for row in table.rows:
            row_content = ''
            for cell in row.cells:
                row_content += cell.text
            table_documents.append(row_content)
    
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

#def extract_docx_text(docx_path: str) -> list:

if __name__ == '__main__':
    docx_path = 'Syllabus-3377-converted.docx'
    table_documents = extract_text_from_tables(docx_path)
    #print(table_documents)
    '''
    table_doc_lemmas = []
    for doc in table_documents:
        table_doc_lemmas.append(preprocess_text(doc))
    '''
    
    '''
    for doc in table_doc_lemmas:
        print(doc + '\n')
    '''
    
    bolded_documents = extract_text_from_bold(docx_path)
    #print(bolded_documents)
    '''
    bolded_doc_lemmas = []
    for doc in bolded_documents:
        bolded_doc_lemmas.append(preprocess_text(doc))
    '''
    
    '''
    for doc in bolded_doc_lemmas:
        print(doc + '\n')
    '''
    
    query = 'grading policy?'
    
    # clean_query = preprocess_text(query)
    # print(clean_query)
    
    matches = get_matching_documents(query, table_documents)
    # output top 5 matches
    for i, match in enumerate(matches[:5]):
        print(str(i) + ': ' + match + '\n')
    
    