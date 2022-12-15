
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
        message = ''
        print(self.path)
        if self.path == '/':
            self.send_header('Content-type', 'text/html')
            file = open('./src/index.html').read()
            message = file
            message = bytes(message, "utf8")
        elif self.path == '/favicon.ico':
            self.send_header('Content-Type', 'image/x-icon')
            file = open('./favicon.ico', 'rb').read()
            message = file
        elif self.path.startswith('/search'):
            self.send_header('Content-type', 'text/html')
            query_components = parse_qs(urlparse(self.path).query, keep_blank_values = True)
            exp = query_components['query'][0]
            books = query_components['type'][0]
            index = int(query_components['queryIndex'][0])
            message = self.search_expression(exp, books == 'Books', index)
            message = bytes(message, "utf8")
        elif self.path.startswith('/open'):
            self.send_header('Content-type', 'text/html')
            try:
                query_components = parse_qs(urlparse(self.path).query)
                path = query_components['path'][0]
                subprocess.call([pdf_reader, path])
                message = 'OK!'
            except:
                message = 'Error!'
            message = bytes(message, "utf8")

        self.end_headers()
        self.wfile.write(message)

    def search_expression(self, expression, book=True, queryIndex=0):
        model = self.model_books if book else self.model_articles
        processed = self.books_processed if book else self.artc_processed
        try:
            result = model.parse(expression)
            qtd = len(result)
            min_index = min(queryIndex * self.numResults, qtd)
            max_index = min((queryIndex+1) * self.numResults, qtd)
            result = [processed[index] for (_, index) in result[min_index:max_index]]
            message = json.dumps({'result': result, 'status': qtd})
            return message
        except:
            return '{}'


print('Starting...')
with HTTPServer(('127.0.0.1', 80), handler) as server:
    print('Running!')
    server.serve_forever()
