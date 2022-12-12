
class Node:
    def __init__(self):
        self.value = None
        self.child = {}

    def hasChild(self, code):
        return code in self.child

    def hasValue(self):
        return self.value is not None


class Trie:
    def __init__(self):
        self.root = Node()

    def get(self, key):
        return self._get(self.root, key, 0)

    def _get(self, root, key, level):
        if level < len(key):
            code = key[level]
            if root.hasChild(code):
                return self._get(root.child[code], key, level + 1)
            else:
                return None
        else:
            return root.value
    
    def _getAll(self, root, key, level):
        if level < len(key):
            code = key[level]
            if root.hasChild(code):
                return self._get(root.child[code], key, level + 1)
            else:
                return []
        else:
            res = [root.value] if root.value else []
            for suf, node in root.child.items():
                res += root._getAll(node, key + suf, level + 1)
            return res

    def put(self, key, value):
        return self._put(key, value, self.root, 0)

    def _put(self, key, value, root, level):
        if level == len(key):
            root.value = value
            return self
        else:
            code = key[level]
            if not root.hasChild(code):
                root.child[code] = Node()
            return self._put(key, value, root.child[code], level + 1)
    
    def __str__(self):
        return self._tostr(self.root, '', 0)
    
    def _tostr(self, node, key, level):
        if node is None:
            return ''
        else:
            res = (' ' * level) + ' {%s, %s} \n' % (key, node.value) if node.value is not None else ''
            for k, n in node.child.items():
                res += self._tostr(n, key + k, level + 1)
            return res
