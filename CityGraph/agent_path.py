import networkx as nx

from CityGraph.graph_tool import path_nodes_to_edges


class AgentPath:
    G = None
    agent_type = None
    path_edges = None
    weight = None
    color = None

    def __init__(self, agent_type, G, source, target, color='red'):
        self.G = G
        self.agent_type = agent_type
        path_nodes = nx.dijkstra_path(G, source, target, weight=self.agent_type)
        self.path_edges = path_nodes_to_edges(path_nodes)
        self.weight = self.compute_weight()
        self.color = color

        print(f'Path {agent_type}: {source} -> {target}')

    # TODO: Unit test this
    def compute_weight(self):
        weights = [self.G[u][v][self.agent_type] for u, v in self.path_edges]
        return sum(weights)
