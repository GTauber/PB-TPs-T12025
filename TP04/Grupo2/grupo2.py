class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        self._collect_words(node, prefix, results)
        return results

    def _collect_words(self, node, prefix, results):
        if node.is_end_of_word:
            results.append(prefix)

        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, results)

    def remove(self, word):
        self._remove_recursive(self.root, word, 0)

    def _remove_recursive(self, node, word, depth):
        if depth == len(word):
            if node.is_end_of_word:
                node.is_end_of_word = False
            return len(node.children) == 0

        char = word[depth]
        if char not in node.children:
            return False

        should_delete_current_node = self._remove_recursive(node.children[char], word, depth + 1)

        if should_delete_current_node:
            del node.children[char]
            return len(node.children) == 0

        return False


def demonstrate_trie():
    trie = Trie()

    words = ["casa", "casamento", "casulo", "cachorro"]
    for word in words:
        trie.insert(word)

    print("Search for 'casa':", trie.search("casa"))
    print("Search for 'apartamento':", trie.search("apartamento"))

    prefix = "cas"
    completions = trie.autocomplete(prefix)
    print(f"Autocomplete for '{prefix}':", completions)

    word_to_remove = "casa"
    print(f"Removing '{word_to_remove}'")
    trie.remove(word_to_remove)

    print("Search for 'casa' after removal:", trie.search("casa"))
    print("Search for 'casamento' after removal:", trie.search("casamento"))
    print("Search for 'casulo' after removal:", trie.search("casulo"))

    completions_after_removal = trie.autocomplete(prefix)
    print(f"Autocomplete for '{prefix}' after removal:", completions_after_removal)


if __name__ == "__main__":
    demonstrate_trie()