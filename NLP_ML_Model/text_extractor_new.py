import PyPDF2
import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from scipy import spatial

stopwords = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_lg') # py -m spacy download en_core_web_lg
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
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

def get_pdf_page_count(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        
        return pdf.numPages


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)

        # get the all document's pages
        text = ''
        for page in pdf.pages:
            text += ''.join(page.extract_text())

        # return a single text string
        return text
    
def extract_text_from_pdf_page(pdf_path, page_num):
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)

        # get one page in the doocument
        text = pdf.pages[page_num].extract_text()

        # return a single text string
        return text

# use spacy to compute similarity between query and each document
def get_matching_document(query, documents):
    error_threshold = 0.5 # similarity score threshold; subject to change
    
    print(query)
    
    query = nlp(preprocess_text(query))
    nlp_docs = []
    for document in documents:
        nlp_docs.append(nlp(preprocess_text(document)))
    
    '''
    print('PAGES')
    for page in nlp_docs:
        print(page.text)
        print('\n\n')
    '''
    
    similarity_scores = [query_similarity := query.similarity(doc) for doc in nlp_docs]
    
    print("Max score: ", max(similarity_scores))
    print("Page number: ", similarity_scores.index(max(similarity_scores)))
    
    if max(similarity_scores) > error_threshold:
        # match found
        most_probable_index = similarity_scores.index(max(similarity_scores))
        most_probable_document = documents[most_probable_index]
        return most_probable_document
    else:
        # no match found
        return None


def get_pdf_text_categories(pdf_path):
    '''
    TODO: Get all text in each section (separated by bolded text lines).
    Put the sections into a list of categories with each element containing
    the bolded text itself along with all the text up until the next bolded text.
    e.g. ['professor contact information dr. karen mazidi email: karen.mazidi@utdallas.edu...']
    '''
    with pdfplumber.open(pdf_path) as pdf:
        for i,page in enumerate(pdf.pages):
            text = pdf.pages[i] # get one page
            
            print(f"______________________Page {i+1} Output______________________")

            # get only bolded words
            #bold_text = text.filter(lambda obj: (obj['object_type'] == 'char' and 'Bold' in obj['fontname']))
            #print(bold_text.extract_text() + '\n')
            
            # get all words
            #text = text.filter(lambda obj: (obj['object_type'] == 'char'))
            #print(text.extract_text(use_text_flow=False) + '\n')
            
            # get italicized words
            #italic_text = text.filter(lambda obj: (obj['object_type'] == 'char' and 'Italic' in obj['fontname']))
            #print(italic_text.extract_text() + '\n')

            #Check object information
            #with open("pdf_info.txt", "a") as f:
            #    print(text.objects, file=f)

            # Extracting Information from Tables
            tablesInfo = text.extract_tables(table_settings={})
            print(tablesInfo)            

if __name__ == '__main__':
    
    # debugging purposes
    pdf_path = 'Syllabus-3377.pdf'
    get_pdf_text_categories(pdf_path)
    '''
    raw_pdf_text = extract_text_from_pdf(pdf_path)
    print(raw_pdf_text)
    print('\n\n\n\n\n')
    
    clean_pdf_text = preprocess_text(raw_pdf_text)
    print(clean_pdf_text)
    print('\n\n\n\n\n')
    '''
    
    '''
    raw_text_pages = []
    for i in range(get_pdf_page_count(pdf_path)):
        raw_text_pages.append(extract_text_from_pdf_page(pdf_path, i))
    
    response = get_matching_document("anyone have tips for starting the word guessing hw?", raw_text_pages)
    print(response)
    print('\n\n\n')
    
    
    
    response = get_matching_document("what are professor's office hours?", raw_text_pages)
    print(response)
    #print('\n\n\n')
    '''
    
    