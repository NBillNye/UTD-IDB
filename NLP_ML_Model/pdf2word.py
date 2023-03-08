from pdf2docx import Converter
import docx
from simplify_docx import simplify

pdf_file = 'Syllabus-3377.pdf'
docx_file = 'Syllabus-3377-converted.docx'

cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close

my_doc = docx.Document('Syllabus-3377-converted.docx')
my_doc_as_json = simplify(my_doc)