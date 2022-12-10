
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.2"

from rpy2.robjects.packages import importr
pdftools = importr('pdftools')

path = r'C:\Users\ivete\Desktop\Lista.pdf'

text = pdftools.pdf_text(path)
text = '\n'.join(text)
