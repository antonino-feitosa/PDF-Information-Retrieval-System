
import re
import math
import heapq
from CreateIndex import *

'''
sts = or_sts or sts | or_Sts
or_sts = and_sts or or_sts | and_sts
and_sts = not_sts and and_sts | not_sts
not_sts = not text | text


'''


class ProcessQuery:
    def __init__(self, tree, num_docs, max_res=10):
        self.tree = tree
        self.num_docs = num_docs
        self.max_res = max_res

    def parse(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        heap = self.parse_or(text)
        result = []
        for _ in range(min(len(heap), self.max_res)):
            result.append(heapq.heappop(heap))
        return result

    def parse_or(self, text):
        res = re.search(' or ', text)
        if res:
            andsts = text[: res.start()]
            orsts = text[res.end():]
            lside, lexclude = self.parse_and(andsts)
            rside, rexclude = self.parse_or(orsts)
            heap = self._union(lside, rside, lexclude, rexclude)
            return heap, False
        else:
            print('or:', text)
            return self.parse_and(text)

    def parse_and(self, text):
        res = re.search(' and ', text)
        if res:
            notsts = text[: res.start()]
            andsts = text[res.end():]
            lside, lexclude = self.parse_not(notsts)
            rside, rexclude = self.parse_and(andsts)
            heap = self._intersect(lside, rside, lexclude, rexclude)
            return heap, False
        else:
            return self.parse_not(text)

    def parse_not(self, text):
        res = re.search('not ', text)
        if res:
            notsts = text[4:]
            return self.parse_text(notsts), True
        else:
            return self.parse_text(text), False

    def parse_text(self, text):
        heap = self.tree.get(text)  # [(-num/max_freq, name),...]
        if heap:
            idf = math.log((self.num_docs + 1)/(len(heap) + 1))
            heap = [(tf * idf, path) for (tf, path) in heap]
            heapq.heapify(heap)
            return heap
        else:
            return []
    
    def _union(self, a_list, b_list, a_exclude, b_exclude):
        result = []
        heapq.heapify(result)
        return result

    def _intersect(self, a_list, b_list, a_exclude, b_exclude):
        if a_exclude and b_exclude:
            return []
        result = []
        if not a_exclude and not b_exclude:
            for (a_value, a_path) in a_list:
                for (b_value, b_path) in b_list:
                    if a_path == b_path:
                        # min priority
                        result.append((min(a_value, b_value), a_path))
        elif a_exclude and not b_exclude:
            
        heapq.heapify(result)
        return result
    
    def _diff(self, a_list, minus_list):
        result = []
        for (a_value, a_path) in a_list:
            for (b_value, b_path) in b_list:
                if a_path == b_path:
                    # min priority
                    result.append((min(a_value, b_value), a_path))
        elif a_exclude and not b_exclude:


# precedence: not and or


def searchQuery(query, tree, num_docs):
    query = re.sub(r'\s+', ' ',   query)			# remove duplicated spaces
    query = query.strip()

    for or_term in query.split('or'):
        or_term = or_term.strip()
        for and_term in or_term:
            and_term.strip()
            if and_term.startswith('not '):
                and_term = and_term[4:-1]


num_documents, tree = loadIndex()

process = ProcessQuery(tree, num_documents)
print(process.parse('algorithm and not genetic'))
