import networkx as nx
import random
import copy

MODIFIER = 4

class BaseStudent:
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.budget = 100
        self.ends = ends
        self.compile_to_graph(edge_list)
        self.lowest_cost_path_set = set()
        self.lowest_cost_path = list()
        self.path_index = 0

    def remove_solitary_edges(self, edge_list):
        out_degree = {}
        out_edges = {}
        for u, v, w in edge_list:
            out_edges[u] = out_edges.get(u, list())
            out_edges[u].append(tuple([v, w]))
            out_degree[u] = out_degree.get(u, 0) + 1
            out_degree[v] = out_degree.get(v, 0)
            
        filtered_edges = []
        for edge in edge_list:
            if out_degree[edge[0]] == 2:
                this_out_edges = out_edges[edge[0]]
                min_edge = min(this_out_edges, key=lambda x: x[1])
                max_edge = max(this_out_edges, key=lambda x: x[1])
                if min_edge[1] == max_edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], min_edge[1] + 2]))
                elif min_edge[0] == edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], min(min_edge[1] + 4, max_edge[1])]))
                elif max_edge[0] == edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], max_edge[1] + 2]))
            elif out_degree[edge[0]] == 3:
                this_out_edges = copy.deepcopy(out_edges[edge[0]])
                min_edge = min(this_out_edges, key=lambda x: x[1])
                this_out_edges.remove(min_edge)
                max_edge = min(this_out_edges, key=lambda x: x[1])
                if min_edge[1] == max_edge[1] == edge[2]:
                    filtered_edges.append(tuple([edge[0], edge[1], min_edge[1] + 1]))
                elif min_edge[0] == edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], min(min_edge[1] + 3, max_edge[1])]))
                elif max_edge[0] == edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], max_edge[1] + 1]))
                else:
                    filtered_edges.append(tuple([edge[0], edge[1], edge[2] + 1]))
            elif out_degree[edge[0]] > 1:
                filtered_edges.append(edge)
        return filtered_edges

    def compile_to_graph(self, edge_list):
        self.graph = nx.DiGraph()
        self.graph_unpruned = nx.DiGraph()
        for u, v, w in edge_list:
            self.graph_unpruned.add_edge(u, v, weight=w)
        mod_edge_list = self.remove_solitary_edges(edge_list)
        for u, v, w in mod_edge_list:
            self.graph.add_edge(u, v, weight=w)
            
    def update_graph(self, edge_updates):
        for edge, weight_increase in edge_updates.items():
            u, v = edge
            self.budget -= weight_increase
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] += weight_increase
                self.graph_unpruned[u][v]['weight'] += weight_increase
            else:
                # should never reach here if we made graph correctly
                pass
    


    def strategy(self, edge_updates, vertex_count, current_vertex):

        self.update_graph(edge_updates)
        shortest_length = 1000

        for u, v, _ in self.edge_list:
            if u == current_vertex:
                # if (self.graph[u][v]['weight'] != self.graph_unpruned[u][v]['weight']):
                #     print("changed smth")
                self.graph[u][v]['weight'] = self.graph_unpruned[u][v]['weight']
        for target_node in range(113, 121):
            try:
                path = nx.shortest_path(self.graph, source=current_vertex, target=target_node, weight='weight')
                path_length = nx.shortest_path_length(self.graph, source=current_vertex, target=target_node, weight='weight')
            except:
                continue
            if path_length < shortest_length:
                self.lowest_cost_path = path
                shortest_length = path_length
        return self.lowest_cost_path[1]




class GreedyStudentShallow(BaseStudent):
    def second_min(self, numbers):
        m1 = m2 = float('inf')
        for x in numbers:
            if x <= m1:
                m1, m2 = x, m1
            elif x < m2:
                m2 = x
        return m2

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.budget = 100
        self.ends = ends
        self.compile_to_graph(edge_list)
        self.lowest_cost_path_set = set()
        self.lowest_cost_path = list()
        self.path_index = 0

    def compile_to_graph(self, edge_list):
        self.graph = nx.DiGraph()
        for u, v, w in edge_list:
            self.graph.add_edge(u, v, weight=w)
            
    def update_graph(self, edge_updates):
        for edge, weight_increase in edge_updates.items():
            u, v = edge
            self.budget -= weight_increase
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] += weight_increase
            else:
                # should never reach here if we made graph correctly
                pass

    def strategy(self, edge_updates, vertex_count, current_vertex):
        self.update_graph(edge_updates)
        targets = list(self.graph[current_vertex].items())
        scores = []

        for target in targets:
            # print(target)
            edge_weights = [w for (_, _, w) in filter(lambda z: z[0] == target[0], self.edge_list)]
            if len(edge_weights) == 1:
                scores.append(self.budget + edge_weights[0] + target[1]['weight'])
            elif len(edge_weights) == 0:
                scores.append(target[1]['weight'])
            else:
                scores.append(min(max(min(edge_weights), self.second_min(edge_weights) - 1), min(edge_weights) + self.budget / 2) + target[1]['weight'])
        
        minimum = min(scores)
        for i in range(len(scores)):
            if minimum == scores[i]:
                return targets[i][0]
        # Take a random out-edge
        # print("this should never be printed")
        return random.choice(
            [
                x
                for (_, x, _) in filter(
                    lambda z: z[0] == current_vertex, self.edge_list
                )
            ]
        )


class GreedyStudent:
    def second_min(self, numbers):
        m1 = m2 = float('inf')
        for x in numbers:
            if x <= m1:
                m1, m2 = x, m1
            elif x < m2:
                m2 = x
        return m2

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.budget = 100
        self.ends = ends
        self.compile_to_graph(edge_list)
        self.lowest_cost_path_set = set()
        self.lowest_cost_path = list()
        self.path_index = 0

    def compile_to_graph(self, edge_list):
        self.graph = nx.DiGraph()
        for u, v, w in edge_list:
            self.graph.add_edge(u, v, weight=w)
            
    def update_graph(self, edge_updates):
        for edge, weight_increase in edge_updates.items():
            u, v = edge
            self.budget -= weight_increase
            if self.graph.has_edge(u, v):
                self.graph[u][v]['weight'] += weight_increase
            else:
                # should never reach here if we made graph correctly
                pass

    def strategy(self, edge_updates, vertex_count, current_vertex):
        self.update_graph(edge_updates)
        # nextv = list(self.graph[current_vertex].items())
        vscores = []
        vvertices = [tuple([v, w]) for (_, v, w) in filter(lambda z: z[0] == current_vertex, self.edge_list)]
        for vertex in vvertices:
            targets = list(self.graph[vertex[0]].items())
            scores = []
            if len(targets) == 1:
                vscores.append(200)
                continue
            for target in targets:
                # print(target)
                edge_weights = [w for (_, _, w) in filter(lambda z: z[0] == target[0], self.edge_list)]
                if len(edge_weights) == 1:
                    scores.append(90 + edge_weights[0] + target[1]['weight'])
                elif len(edge_weights) == 0:
                    scores.append(target[1]['weight'])
                else:
                    scores.append(min(edge_weights) + target[1]['weight'])
            # print(i)
            # print(len(vweights))
            if len(scores) == 0:
                vscores.append(vertex[1])
            else:
                vscores.append(min(scores) + vertex[1])
        vmin = min(vscores)
        for i in range(len(vscores)):
            if vmin == vscores[i]:
                return vvertices[i][0]
        # Take a random out-edge
        # print("this should never be printed")
        return random.choice(
            [
                x
                for (_, x, _) in filter(
                    lambda z: z[0] == current_vertex, self.edge_list
                )
            ]
        )


# Greedy Strategy
class RandomStudent(BaseStudent):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def strategy(self, edge_updates, vertex_count, current_vertex):

        # Take a random out-edge
        return random.choice(
            [
                x
                for (_, x, _) in filter(
                    lambda z: z[0] == current_vertex, self.edge_list
                )
            ]
        )


# Modified strategy
class PrunedStudent(BaseStudent):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.budget = 100
        self.ends = ends
        self.compile_to_graph(edge_list)
        self.lowest_cost_path_set = set()
        self.lowest_cost_path = list()
        self.path_index = 0

    def remove_solitary_edges(self, edge_list):
        out_degree = {}
        out_edges = {}
        for u, v, w in edge_list:
            out_edges[u] = out_edges.get(u, list())
            out_edges[u].append(tuple([v, w]))
            out_degree[u] = out_degree.get(u, 0) + 1
            out_degree[v] = out_degree.get(v, 0)
            
        filtered_edges = []
        for edge in edge_list:
            if out_degree[edge[0]] > 1:
                filtered_edges.append(edge)
        return filtered_edges
    

class PrunedStudent1(BaseStudent):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.budget = 100
        self.ends = ends
        self.compile_to_graph(edge_list)
        self.lowest_cost_path_set = set()
        self.lowest_cost_path = list()
        self.path_index = 0

    def remove_solitary_edges(self, edge_list):
        out_degree = {}
        out_edges = {}
        for u, v, w in edge_list:
            out_edges[u] = out_edges.get(u, list())
            out_edges[u].append(tuple([v, w]))
            out_degree[u] = out_degree.get(u, 0) + 1
            out_degree[v] = out_degree.get(v, 0)
            
        filtered_edges = []
        for edge in edge_list:
            if out_degree[edge[0]] == 2:
                this_out_edges = out_edges[edge[0]]
                min_edge = min(this_out_edges, key=lambda x: x[1])
                max_edge = max(this_out_edges, key=lambda x: x[1])
                if min_edge[1] == max_edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], min_edge[1] + 2]))
                elif min_edge[0] == edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], min(min_edge[1] + 4, max_edge[1])]))
                elif max_edge[0] == edge[1]:
                    filtered_edges.append(tuple([edge[0], edge[1], max_edge[1] + 2]))
            elif out_degree[edge[0]] > 1:
                filtered_edges.append(edge)
        return filtered_edges