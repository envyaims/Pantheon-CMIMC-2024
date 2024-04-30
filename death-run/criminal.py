import networkx as nx
import random
from math import floor


class BaseCriminal:
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.lowest_cost_path = None
        self.second_cost_path = None
        self.compile_to_graph(edge_list)
        self.ends = ends
    
    def compile_to_graph(self, edge_list):
        self.graph = nx.DiGraph()
        for u, v, w in edge_list:
            self.graph.add_edge(u, v, weight=w)
            
    def update_graph(self, edge_updates):
        for edge, weight_increase in edge_updates.items():
            u, v = edge
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] += weight_increase
            else:
                # should never reach here if we made graph correctly
                pass

    def strategy(self, edge_updates, vertex_count, budget):
        # update graph from last iteration of strategy
        self.update_graph(edge_updates)
        
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )

        scores = []
        vertex_scores = {}
        path = None
        path_length = None
        shortest_length = 1000
        second_length = 1000

        for vertex in populated_vertices:
            shortest_length = 1000
            for target_node in range(113, 121):
                try:
                    path = nx.shortest_path(self.graph, source=vertex, target=target_node, weight='weight')
                    path_length = nx.shortest_path_length(self.graph, source=vertex, target=target_node, weight='weight')
                except:
                    continue
                if path_length < shortest_length:
                    self.lowest_cost_path = path
                    shortest_length = path_length

            # Modify the weight of the first edge to a large value
            if len(self.lowest_cost_path) > 1:
                u, v = self.lowest_cost_path[0], self.lowest_cost_path[1]
                original_weight = self.graph[u][v]['weight']
                self.graph[u][v]['weight'] = 1000  # or any large value

            for target_node in range(113, 121):
                try:
                    path = nx.shortest_path(self.graph, source=vertex, target=target_node, weight='weight')
                    path_length = nx.shortest_path_length(self.graph, source=vertex, target=target_node, weight='weight')
                except:
                    continue

                if path_length < second_length:
                    self.second_cost_path = path
                    second_length = path_length

            # Reset the weight of the modified edge
            if len(self.lowest_cost_path) > 1:
                self.graph[u][v]['weight'] = original_weight  # Reset to original weight
            scores.append((vertex, self.lowest_cost_path[1], (second_length - shortest_length - 1) * vertex_count[vertex] * 0.5))





            targets = [(s, x, w) for (s, x, w) in filter(lambda z: z[0] == vertex, self.edge_list)]
            vertex_scores[vertex] = vertex_scores.get(vertex, 0) + 1 / len(targets)
            if len(targets) == 1:
                if vertex_count[vertex] >= 2:
                    return (vertex, targets[0][1], budget)
                elif vertex_count[vertex] == 1:
                    return (vertex, targets[0][1], 0.9 * budget)
            else:
                minimum = 1000
                min_target = -1
                min_src = -1
                min_index = -1
                second_min = 1000
            
                for i in range(len(targets)):
                    if targets[i][2] <= minimum:
                        minimum = targets[i][2]
                        min_target = targets[i][1]
                        min_src = targets[i][0]
                        # print(min_src, min_target)
                        min_index = i
                for i in range(len(targets)):
                    if (targets[i][2] < second_min and targets[i][2] > minimum):
                        second_min = targets[i][2]
                    elif targets[i][2] == minimum and i != min_index:
                        second_min = minimum
                        break
                # print((second_min - minimum - 1))
                scores.append((min_target, min_src, (second_min - minimum) * vertex_count[min_src]))

        key = max(scores, key=lambda p: p[2])
        # print(key[2])
        # print(populated_vertices)
        if populated_vertices[0] >= 105 and key[2] <= 0:
            most_attractive = max(vertex_scores, key=vertex_scores.get)
            targets = [(s, x, w) for (s, x, w) in filter(lambda z: z[0] == most_attractive, self.edge_list)]
            min_weight_target = min(targets, key=lambda t: t[2])
            return (most_attractive, min_weight_target[1], budget)
        if key[2] <= 0:
            most_attractive = max(vertex_scores, key=vertex_scores.get)
            targets = [(s, x, w) for (s, x, w) in filter(lambda z: z[0] == most_attractive, self.edge_list)]
            min_weight_target = min(targets, key=lambda t: t[2])
            return (most_attractive, min_weight_target[1], min(floor(vertex_count[key[1]] / len(targets)), budget))
        if vertex_count[key[1]] != 0:
            return (key[1], key[0], min(key[2] / vertex_count[key[1]], budget))
        
        return (key[1], key[0], 0)





# Starter strategy
class RandomCriminal(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def strategy(self, edge_updates, vertex_count, budget):
        # Find a random populated vertex
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )
        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            random.randint(0, budget),
        )


# Starter strategy
class BetterCriminal(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.compile_to_graph(edge_list)
        self.ends = ends
    
    def compile_to_graph(self, edge_list):
        self.graph = nx.DiGraph()
        for u, v, w in edge_list:
            self.graph.add_edge(u, v, weight=w)
            
    def update_graph(self, edge_updates):
        for edge, weight_increase in edge_updates.items():
            u, v = edge
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] += weight_increase
            else:
                # should never reach here if we made graph correctly
                pass

    def strategy(self, edge_updates, vertex_count, budget):
        # update graph from last iteration of strategy
        self.update_graph(edge_updates)
        
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )

        scores = []

        for vertex in populated_vertices:
            targets = [(s, x, w) for (s, x, w) in filter(lambda z: z[0] == vertex, self.edge_list)]
            if len(targets) == 1:
                if vertex_count[vertex] >= 2:
                    return (vertex, targets[0][1], budget)
                elif vertex_count[vertex] == 1:
                    return (vertex, targets[0][1], (budget / 1.5))
            else:
                minimum = 1000
                min_target = -1
                min_src = -1
                second_min = 1000
                for i in range(len(targets)):
                    if targets[i][2] < minimum:
                        minimum = targets[i][2]
                        min_target = targets[i][1]
                        min_src = targets[i][0]
                        second_min = minimum
                scores.append((min_target, min_src, (second_min - minimum - 1) * vertex_count[min_src]))
        # Fill in random out-edge with random weight
        key = min(scores, key=lambda p: p[2])
        return (key[0], key[1], min(key[2] / vertex_count[key[1]], budget / 2))
    
    def dfs_lowest_cost_path(graph, current_vertex, target_vertices):
        # Initialize variables to keep track of visited vertices and the lowest cost path found so far
        visited = set()
        lowest_cost_path = None

        # Define a recursive DFS function
        def dfs_util(vertex, path, cost):
            nonlocal lowest_cost_path
            
            # Mark the current vertex as visited
            visited.add(vertex)

            # If the current vertex is one of the target vertices, update the lowest cost path
            if vertex in target_vertices:
                if lowest_cost_path is None or cost < lowest_cost_path[1]:
                    lowest_cost_path = (path, cost)

            # Explore neighbors
            for neighbor, attrs in graph[vertex].items():
                if neighbor not in visited:
                    # Recursively call DFS for unvisited neighbors
                    dfs_util(neighbor, path + [neighbor], cost + attrs['weight'])

        # Start DFS from the current vertex
        dfs_util(current_vertex, [current_vertex], 0)

        return lowest_cost_path

