
from Trie import *

def test_trie():
    trie = Trie()
    trie.put('machine', 1)
    trie.put('machine 2', 3)
    trie.put('machine 3', 4)
    assert trie.get('machine') == 1
    assert trie.get('machine 2') == 3
    assert trie.get('machine 3') == 4
    trie.put('put', 3)
    trie.put('machine', 2)
    assert trie.get('put') == 3
    assert trie.get('machine') == 2
