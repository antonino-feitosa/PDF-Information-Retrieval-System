
from Trie import *

def test_trie():
    trie = Trie()
    trie.add('machine', 1)
    trie.add('machine 2', 3)
    trie.add('machine 3', 4)
    assert trie.get('machine') == 1
    assert trie.get('machine 2') == 3
    assert trie.get('machine 3') == 4
    trie.add('add', 3)
    trie.add('machine', 2)
    assert trie.get('add') == 3
    assert trie.get('machine') == 2
