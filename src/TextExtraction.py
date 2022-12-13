
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.2"

from rpy2.robjects.packages import importr
pdftools = importr('pdftools')
png = importr('png')

def extractPDF(fileName):
    try:
        text = pdftools.pdf_text(fileName)
        text = '\n'.join(text)
        return text
    except:
        return None

def extractThumbnail(fileName):
    try:
        bitmap = pdftools.pdf_render_page(fileName, page = 1)
        index_w = fileName.rfind('/')
        index_l = fileName.rfind('\\')
        index = max(0, index_w, index_l)
        thmbName = './thumbnails/' + fileName[index:-4] + '.png'
        png.writePNG(bitmap, thmbName)
        return thmbName
    except:
        return None

