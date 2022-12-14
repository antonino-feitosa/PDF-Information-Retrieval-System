
# install.packages("pdftools")

library("pdftools")

extractPDF <- function(fileName){
	pdf.text <- pdftools::pdf_text(fileName);
	return(cat(paste(pdf.text[])));
}

fileName <- r'(C:\Users\anton\Documents\Books\[Literatura]\A Brief History of Time.pdf)';
pdf.text <- pdftools::pdf_text(fileName)
cat(paste(pdf.text[2]))

bitmap <- pdf_render_page(fileName, page = 1)
png::writePNG(bitmap, "page.png")
?writePNG

r <- png::writePNG(bitmap, raw())
r <- png::readPNG(r)



install.packages("imager")
library(imager)



?pdf_convert



#cat(extractPDF(fileName))


