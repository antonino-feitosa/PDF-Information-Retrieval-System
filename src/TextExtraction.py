
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

base = importr('base')
pdftools = importr('pdftools')

robjects.r('''
	extractPDF <- function(fileName){
		pdf.text <- pdftools::pdf_text(fileName);
		return(cat(paste(pdf.text[])));
	}
''')


path = r'C:\Users\anton\Documents\Books\A First Course in Combinatorial Optimization.pdf'

text = robjects.r['extractPDF'](path)


