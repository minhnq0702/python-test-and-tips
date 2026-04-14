from PyPDF2 import PdfFileReader

pdf = PdfFileReader(open('hdld.pdf', 'rb'), strict=False)
print(pdf.numPages)
doc_info = pdf.getDocumentInfo()
print(doc_info)
for page in pdf.pages:
    print("==>", page)
    p_w = float(page.mediaBox.getUpperRight_x())
    p_h = float(page.mediaBox.getUpperRight_y())
    print(p_w, p_h)
