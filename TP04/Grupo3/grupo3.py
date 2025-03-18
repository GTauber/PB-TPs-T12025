class Graph:
    def __init__(self, is_directed=False):
        self.adj_list = {}
        self.is_directed = is_directed

    def add_edge(self, u, v):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []

        self.adj_list[u].append(v)
        if not self.is_directed:
            self.adj_list[v].append(u)

    def build_from_edges(self, edges):
        for u, v in edges:
            self.add_edge(u, v)

    def dfs(self, start):
        visited = []
        self._dfs_helper(start, visited, set())
        return visited

    def _dfs_helper(self, node, visited, visited_set):
        visited.append(node)
        visited_set.add(node)

        for neighbor in self.adj_list[node]:
            if neighbor not in visited_set:
                self._dfs_helper(neighbor, visited, visited_set)

    def bfs(self, start):
        visited = []
        queue = [start]
        visited_set = set([start])

        while queue:
            node = queue.pop(0)
            visited.append(node)

            for neighbor in self.adj_list[node]:
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    queue.append(neighbor)

        return visited

    def find_path(self, start, end, algorithm="bfs"):
        if algorithm not in ["bfs", "dfs"]:
            raise ValueError("Algorithm must be 'bfs' or 'dfs'")

        if start not in self.adj_list or end not in self.adj_list:
            return None

        if start == end:
            return [start]

        visited = set()
        path = {}

        if algorithm == "bfs":
            queue = [start]
            visited.add(start)

            while queue:
                node = queue.pop(0)

                for neighbor in self.adj_list[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        path[neighbor] = node
                        queue.append(neighbor)

                        if neighbor == end:
                            break
        else:
            self._dfs_path_helper(start, end, visited, path)

        if end not in path and start != end:
            return None

        result = []
        current = end

        while current != start:
            result.append(current)
            current = path[current]

        result.append(start)
        result.reverse()

        return result

    def _dfs_path_helper(self, node, end, visited, path):
        visited.add(node)

        if node == end:
            return True

        for neighbor in self.adj_list[node]:
            if neighbor not in visited:
                path[neighbor] = node
                if self._dfs_path_helper(neighbor, end, visited, path):
                    return True

        return False


def demonstrate_graph_operations():
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]

    graph = Graph(is_directed=False)
    print("Ex 3.1")
    graph.build_from_edges(edges)

    print("Graph representation (adjacency list):")
    for node in sorted(graph.adj_list.keys()):
        print(f"{node}: {graph.adj_list[node]}")

    print("Ex 3.2")
    print("\nDFS starting from A:")
    dfs_result = graph.dfs('A')
    print(" -> ".join(dfs_result))

    print("Ex 3.3")
    print("\nBFS starting from A:")
    bfs_result = graph.bfs('A')
    print(" -> ".join(bfs_result))

    start_node = 'A'
    end_node = 'E'
    print("Ex 3.4")
    print(f"\nPath from {start_node} to {end_node} using BFS:")
    path = graph.find_path(start_node, end_node, "bfs")
    if path:
        print(" -> ".join(path))
    else:
        print(f"No path exists from {start_node} to {end_node}")

    start_node = 'A'
    end_node = 'E'
    print(f"\nPath from {start_node} to {end_node} using DFS:")
    path = graph.find_path(start_node, end_node, "dfs")
    if path:
        print(" -> ".join(path))
    else:
        print(f"No path exists from {start_node} to {end_node}")


if __name__ == "__main__":
    demonstrate_graph_operations()