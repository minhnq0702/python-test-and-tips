from PyPDF2 import PdfReader

pdf = PdfReader('157563HD3.pdf')
page = pdf.pages[0].rotation
print(page)
# if page.right - page.right > page.getUpperRight_y() - page.getLowerRight_y():
#     print('Landscape')
# else:
#     print('Portrait')