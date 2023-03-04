import PyPDF2
import openai
import pprint
import nltk
from nltk.tokenize import word_tokenize
import os
import spacy

'''
Obtain a personal API key from openai
Run this command in the terminal
export OPENAI_API_KEY='your_openai_api_key'
'''
openai.api_key = os.environ.get("OPENAI_API_KEY")

def preprocess_text(text):
    # remove extra spaces, newlines, tabs
    text = nltk.re.sub(r'\s+', ' ', text).strip()
    text = text.replace('\n', '').replace('\t', '')

    #return a single text string
    return text

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
    
def get_token_count(text):
    '''
    using openai's token count will reduce ambiguity for parameters 
    such as max_tokens, n, etc.
    e.g. compared to nltk's token count
    '''
    result = openai.Completion.create(
        engine="davinci",
        prompt=f"Count the tokens in the following text:\n{text}",
        max_tokens=1,
        n=1,
        stop=None
    )

    response = result.choices[0].text
    tokens = word_tokenize(response)

    # return an int
    return len(tokens)

# NOTE: consider returning a list of matching documents if they are all within threshold?

def get_matching_document(query, document_list):
    error_threshold = 0.75 # similarity score threshold; subject to change
    
    # semantically search through all documents
    results = openai.Completion.create(
        engine='davinci',
        prompt=query,
        max_tokens = 10,
        n=1,
        stop=None,
        temperature=0.2,
        search_model="ada",
        documents=document_list
    )
    
    print("Score: ", results.choices[0].score)
    
    # check the most related document against a threshold
    if results.choices[0].score > error_threshold:
        # match found
        matched_doc = document_list[results.choices[0].index]

        return matched_doc
    else:
        # no match within threshold found
        return None


if __name__ == '__main__':
    # debugging purposes
    pdf_path = 'Syllabus-4375.pdf'
    raw_pdf_text = extract_text_from_pdf(pdf_path)
    print(raw_pdf_text)
    print('\n\n\n\n\n')
    clean_pdf_text = preprocess_text(raw_pdf_text)

    print(clean_pdf_text)
    print('\n\n\n\n\n')

    response = get_matching_document("anyone have tips for starting the word guessing hw?", list(clean_pdf_text))

    print('\n\n\n')
    pprint.pprint(response)

    response = get_matching_document("what are professor's office hours?", list(clean_pdf_text))

    print('\n\n\n')
    pprint.pprint(response)