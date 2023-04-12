from text_extractor_docx import *
from pipeline import *

if __name__ == '__main__':
    docx_path = '/NLP_ML_Model/Syllabus-3377-converted.docx'
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
                    #print(f'Added doc keywords: {doc_keywords}')

    # map keywords to documents
    doc_dict = {}
    for doc in all_docs:
        doc_dict[' '.join(doc.keywords)] = doc.text
    
    print(f'Transformed query: {query_keywords}') 
    matches = get_matching_documents(' '.join(query_keywords), only_key_docs)
    # output top 5 matches
    for i, match in enumerate(matches[:5]):
        context = str(i) + ': ' + doc_dict[match] + '\n'
    ##print(context)
    Pipeline.get_answer(query, context)
    