import datetime

import hyperopt
from hyperopt import fmin, tpe, hp

from CityGraph.agent_path import AgentPath
from CityGraph.edge_type import EdgeType


from CityGraph.graph_drawer import Drawer
from CityGraph.graph_tool import find_node_by_edge_type


def update_edge_type(G, edge, new_type):
    G[edge[0]][edge[1]]['type'] = new_type
    EdgeType.set_weight(G)

class Agent:
    def __init__(self, agent_type: str, src_node, dest_type):
        self.agent_type = agent_type
        self.src_node = src_node
        self.dest_type = dest_type

    def best_paths(self, G):
        targets = find_node_by_edge_type(G, self.dest_type)
        print(targets)

class Optimizer:
    def __init__(self, graph, source_pedestrian, source_car, target):
        self.graph = graph
        self.G = graph.G
        self.source_pedestrian = source_pedestrian
        self.source_car = source_car
        self.target = target

    def space(self):
        space = {}
        hyperopt_choices = ['office', 'park', 'residence', 'commerce', 'connector']
        for u, v, d in self.G.edges(data=True):
            if d['type'] in hyperopt_choices:
                edge = (u, v)
                space[edge] = hp.choice(str(edge), hyperopt_choices)


        return space

    def compute_score(self):
        target_residence = next(iter(find_node_by_edge_type(self.G, 'residence')), self.target)
        target_office = next(iter(find_node_by_edge_type(self.G, 'office')), self.target)
        pedestrian_path = AgentPath('Pedestrian', self.G, self.source_pedestrian, target_residence, 'red')
        car_driver_path = AgentPath('Car driver', self.G, self.source_car, target_office, 'blue')

        # Draw maps
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
        file_path = f'../out/gen/gen_{datetime_str}.png'
        graph_drawer = Drawer(self.graph, dpi=200, node_size=0, edge_size=2)
        graph_drawer.static_agents_paths([pedestrian_path, car_driver_path], file_path)

        return car_driver_path.weight + pedestrian_path.weight

    # define an objective function
    def objective(self, args):
        # TODO: Optimize with set_edge_attributes
        for edge, new_edge_type in args.items():
            update_edge_type(self.G, edge, new_edge_type)
        return self.compute_score()

    def optimize(self, max_evals=100):
        # define a search space
        space = self.space()

        # minimize the objective over the space
        best = fmin(self.objective, space, algo=tpe.suggest, max_evals=max_evals)

        # Set graph to best params
        print(hyperopt.space_eval(space, best))
        self.objective(hyperopt.space_eval(space, best))
