
# install.packages("pdftools")

library("pdftools")

extractPDF <- function(fileName){
	pdf.text <- pdftools::pdf_text(fileName);
	return(cat(paste(pdf.text[])));
}


#fileName <- 'C:\\Users\\anton\\Documents\\Books\\A First Course in Combinatorial Optimization.pdf';

#cat(extractPDF(fileName))


