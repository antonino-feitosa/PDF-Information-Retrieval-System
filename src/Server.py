
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse, unquote

from CreateIndex import *
from Queries import *

pdf_reader = r'C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitPDFReader.exe'

class handler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.numResults = 10

        self.books_processed, self.books_tree = loadIndex(
            './data_index_books.dat')
        self.model_books = ProcessQuery(self.books_tree, self.books_processed)

        self.artc_processed, self.artc_tree = loadIndex(
            './data_index_articles.dat')
        self.model_articles = ProcessQuery(self.artc_tree, self.artc_processed)

        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = ''
        print(self.path)
        if self.path == '/':
            file = open('./src/index.html').read()
            message = file
            message = bytes(message, "utf8")
        elif self.path == '/favicon.ico':
            file = open('./favicon.ico', 'rb').read()
            self.send_header('Content-Type', 'image/x-icon')
            #self.send_header('Content-Length', len(file))
            self.end_headers()
            message = file
        elif self.path.startswith('/search'):
            query_components = parse_qs(urlparse(self.path).query)
            exp = query_components['query'][0]
            books = query_components['type'][0]
            index = int(query_components['queryIndex'][0])
            message = self.search_expression(exp, books == 'Books', index)
            message = bytes(message, "utf8")
        elif self.path.startswith('/open'):
            try:
                query_components = parse_qs(urlparse(self.path).query)
                path = query_components['path'][0]
                subprocess.call([pdf_reader, path])
                message = 'OK!'
            except:
                message = 'Error!'
            message = bytes(message, "utf8")
            
        self.wfile.write(message)

    def search_expression(self, expression, book=True, queryIndex=0):
        model = self.model_books if book else self.model_articles
        try:
            result = model.parse(expression)
            qtd = len(result)
            min_index = min(queryIndex * self.numResults, qtd)
            max_index = min((queryIndex+1) * self.numResults, qtd)
            result = [path for (_, path) in result[min_index:max_index]]
            message = json.dumps({'result': result, 'status': qtd})
            return message
        except:
            return '{}'


print('Starting...')
with HTTPServer(('127.0.0.1', 80), handler) as server:
    print('Running!')
    server.serve_forever()
