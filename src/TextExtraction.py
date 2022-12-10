
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.2"

from rpy2.robjects.packages import importr
pdftools = importr('pdftools')

def extractPDF(fileName):
	text = pdftools.pdf_text(fileName)
	text = '\n'.join(text)
	return text
