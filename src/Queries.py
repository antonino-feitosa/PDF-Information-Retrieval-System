
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
    def __init__(self, tree, processed, max_res=10):
        self.tree = tree
        self.processed = processed
        self.num_docs = len(processed)
        self.max_res = max_res

    def parse(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        heap, _ = self.parse_or(text)
        result = []
        count = 0
        while count < self.max_res and heap:
            result.append(heapq.heappop(heap))
            count += 1
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
        result, handle = self._handle_exclude(
            a_list, b_list, a_exclude, b_exclude)
        if not handle:
            for (a_value, a_path) in a_list:
                b_value = self._contains(a_path, b_list)
                if b_value:
                    a_value = min(a_value, b_value) # min priority
                result.append((a_value, a_path))
            for (b_value, b_path) in b_list:
                if not self._contains(b_path, a_list):
                    result.append((b_value, b_path))
            heapq.heapify(result)
        return result

    def _intersect(self, a_list, b_list, a_exclude, b_exclude):
        result, handle = self._handle_exclude(
            a_list, b_list, a_exclude, b_exclude)
        if not handle:
            for (a_value, a_path) in a_list:
                b_value = self._contains(a_path, b_list)
                if b_value:  # min priority
                    result.append((min(a_value, b_value), a_path))
            heapq.heapify(result)
        return result

    def _handle_exclude(self, a_list, b_list, a_exclude, b_exclude):
        if a_exclude and not b_exclude:
            return self._diff(b_list, a_list), True
        elif not a_exclude and b_exclude:
            return self._diff(a_list, b_list), True
        elif a_exclude and b_exclude:
            return [], True
        return [], False

    def _diff(self, a_list, minus_list):
        result = []
        for (value, path) in a_list:
            if not self._contains(path, minus_list):
                result.append((value, path))
        heapq.heapify(result)
        return result

    def _contains(self, path, list):
        for (v, x) in list:
            if x == path:
                return v
        return None



#num_documents, tree = loadIndex()

#process = ProcessQuery(tree, num_documents)
#print(process.parse('algorithm'))
#print(process.parse('genetic'))
#print(process.parse('algorithm or genetic'))
#print(process.parse('algorithm and genetic'))
#print(process.parse('algorithm and not genetic or math and not math'))
#