import PyPDF2
import openai
import pprint
import nltk
from nltk.tokenize import word_tokenize

# TEMPORARY | move this secret api key (or future ones) into a file and store it privately into the database
openai.api_key = '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'

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

# TODO: appears to be ineffective, must redo using openai's .search for semantic search engine
def get_document_probability(query, document_text):
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Is the following query:\n{query}\n\n relevant to the following text:\n{document_text}\n\n Give me a floating point between 0 (no) to 1 (yes)",
        max_tokens=10,
        n=1,
        temperature = 0.5,
        stop=None
    )

    response = response.choices[0].text
    tokens = word_tokenize(response)
    
    print(tokens)
    
    # return the first (most probable) single token response
    return tokens[0]

''''
def get_classifications(text):
    response = openai.Completion.create(
        engine="babbage",
        prompt=f"classify the following university course syllabus:\n{text}\n\ninto categories f:",
        max_tokens=get_token_count(text)+20,
        n=10,
        stop=None,
        temperature=0.5
    )
    categories = response["choices"][0]["text"].strip().split("\n")
    return categories
'''

if __name__ == '__main__':
    # debugging purposes
    pdf_path = 'Syllabus-4375.pdf'
    raw_pdf_text = extract_text_from_pdf(pdf_path)
    print(raw_pdf_text)
    print('\n\n\n\n\n')
    clean_pdf_text = preprocess_text(raw_pdf_text)

    print(clean_pdf_text)
    print('\n\n\n\n\n')

    response = get_document_probability("anyone have tips for starting the word guessing hw?", clean_pdf_text)

    print('\n\n\n')
    pprint.pprint(response)

    response = get_document_probability("what are professor's office hours?", clean_pdf_text)

    print('\n\n\n')
    pprint.pprint(response)