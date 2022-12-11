
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

    def add(self, key, value):
        return self._add(key, value, self.root, 0)

    def _add(self, key, value, root, level):
        if level == len(key):
            root.value = value
            return self
        else:
            code = key[level]
            if not root.hasChild(code):
                root.child[code] = Node()
            return self._add(key, value, root.child[code], level + 1)
