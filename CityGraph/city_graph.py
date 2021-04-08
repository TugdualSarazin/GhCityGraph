import networkx as nx
import numpy as np


class Metric:
    key = None
    name = None


class AgentType:
    key: str
    name: str
    metric_factor: {Metric: float}


class CityGraph:
    def __init__(self, G: nx.Graph, agent_types=[], geo_graph=True):
        self.G = G
        self.agent_types = agent_types
        self.geo_graph = geo_graph
        self.pos = self.pos()

    # TODO: need unit test
    def pos(self):
        is_geo = True
        for node in self.G.nodes():
            if not (type(node) == tuple and type(node[0]) == float and type(node[1]) == float):
                # TODO: raise error
                is_geo = False
                break
        if self.geo_graph:
            return dict([(n, np.array(n)) for n in self.G.nodes()])
        else:
            return nx.spring_layout(self.G)
