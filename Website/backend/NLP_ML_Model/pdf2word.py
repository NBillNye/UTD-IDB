from pdf2docx import Converter
import docx
from simplify_docx import simplify

def pdf2docx(pdf_path: str):
    cv = Converter(pdf_path)
    
    pdf_path = pdf_path[:len(pdf_path)-4]
    docx_path = pdf_path + '-converted.docx'

    cv.convert(docx_path)
    cv.close


if __name__ == '__main__':
    '''
    pdf_file = 'Syllabus-3377.pdf'
    docx_file = 'Syllabus-3377-converted.docx'

    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close

    my_doc = docx.Document('Syllabus-3377-converted.docx')
    my_doc_as_json = simplify(my_doc)
    '''
    pdf2docx('Syllabus-3377.pdf')
    pdf2docx('Syllabus-4375.pdf')