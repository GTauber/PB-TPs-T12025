import matplotlib.pyplot as plt
import time
import random
import string
import networkx as nx

from TP04.Grupo2.grupo2 import Trie


def generate_random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_dataset(num_words, word_length):
    return [generate_random_word(word_length) for _ in range(num_words)]


def measure_trie_operations(sizes):
    insert_times = []
    search_times = []
    autocomplete_times = []
    remove_times = []

    for size in sizes:
        words = generate_dataset(size, 10)

        trie = Trie()

        start = time.time()
        for word in words:
            trie.insert(word)
        end = time.time()
        insert_times.append(end - start)

        search_words = words[:100] if len(words) > 100 else words
        start = time.time()
        for word in search_words:
            trie.search(word)
        end = time.time()
        search_times.append((end - start) / len(search_words))

        prefixes = [word[:3] for word in search_words]
        start = time.time()
        for prefix in prefixes:
            trie.autocomplete(prefix)
        end = time.time()
        autocomplete_times.append((end - start) / len(prefixes))

        remove_words = words[:100] if len(words) > 100 else words
        start = time.time()
        for word in remove_words:
            trie.remove(word)
        end = time.time()
        remove_times.append((end - start) / len(remove_words))

    return insert_times, search_times, autocomplete_times, remove_times


def plot_time_complexity():
    sizes = [100, 500, 1000, 2000, 5000]
    insert_times, search_times, autocomplete_times, remove_times = measure_trie_operations(sizes)

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.plot(sizes, insert_times, 'o-', label='Insert')
    plt.title('Insert Operation Time')
    plt.xlabel('Number of Words')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(sizes, search_times, 's-', label='Search')
    plt.title('Search Operation Time (per word)')
    plt.xlabel('Number of Words in Trie')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(sizes, autocomplete_times, '^-', label='Autocomplete')
    plt.title('Autocomplete Operation Time (per prefix)')
    plt.xlabel('Number of Words in Trie')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(sizes, remove_times, 'd-', label='Remove')
    plt.title('Remove Operation Time (per word)')
    plt.xlabel('Number of Words in Trie')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('trie_complexity.png')
    plt.show()


def visualize_trie_structure():
    trie = Trie()
    words = ["casa", "casamento", "casulo", "cachorro"]
    for word in words:
        trie.insert(word)

    plt.figure(figsize=(12, 8))
    G = nx.DiGraph()

    def add_nodes(node, prefix, parent_id=None):
        current_id = prefix if prefix else "root"
        if parent_id is not None:
            G.add_edge(parent_id, current_id)

        for char, child in node.children.items():
            new_prefix = prefix + char
            add_nodes(child, new_prefix, current_id)

    add_nodes(trie.root, "")

    pos = nx.spring_layout(G, seed=42)
    node_colors = ['red' if node == 'root' else 'lightblue' for node in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=1500, font_size=10, arrows=True)

    plt.title("Trie Structure Visualization")
    plt.savefig('trie_structure.png')
    plt.show()

plot_time_complexity()
visualize_trie_structure()