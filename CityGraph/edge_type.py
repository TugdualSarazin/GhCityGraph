class EdgeType:
    # TODO: move to DEFAULT WEIGHT config
    weight_config = {
        'Noise': {
            'agent_type': {
                'Pedestrian': 20,
                'Car driver': 0,
            }
        },
        'Traffic': {
            'agent_type': {
                'Pedestrian': 0,
                'Car driver': 20,
            }
        },
        'Tree index': {
            'agent_type': {
                'Pedestrian': -20,
                'Car driver': 0,
            }
        },
        'Traffic light': {
            'agent_type': {
                'Pedestrian': 10,
                'Car driver': 10,
            }
        },
        'Sidewalk': {
            'agent_type': {
                'Pedestrian': -10,
                'Car driver': 0,
            }
        },
        'Commerce': {
            'agent_type': {
                'Pedestrian': 0,
                'Car driver': 0,
            }
        },
        'Street light index': {
            'agent_type': {
                'Pedestrian': -2,
                'Car driver': 0,
            }
        },
        'Crosswalk': {
            'agent_type': {
                'Pedestrian': 20,
                'Car driver': 20,
                #'Car driver': 10000,
            }
        },
        'Sidewalk obstacles': {
            'agent_type': {
                'Pedestrian': 30,
                'Car driver': 0,
            }
        },
    }

    weight_keys = sorted(set(weight_config))
    # agent_keys = {'Pedestrian', 'biker'}
    agent_keys = {'Pedestrian', 'Car driver'}
    edge_types = {'Connector', 'Cross', 'Overpass', 'Road', 'Underpass'}

    @staticmethod
    def set_weight(G):
        EdgeType.set_edge_type_weights(G)
        EdgeType.set_agent_type_weights(G)

    # Length: length in meters
    @staticmethod
    def set_edge_type_weights(G):
        # Iterate edges
        for u, v, d in G.edges(data=True):
            # TODO: Assert errors not find
            etype = d['type']
            length = d['length']

            # Iterate weight keys
            for wkey in EdgeType.weight_keys:
                try:
                    attr_factor = EdgeType.weight_config[wkey]['type'][etype]
                    # Set edge attr value
                    G[u][v][wkey] = length * attr_factor
                except KeyError:
                    # TODO: unit test exception
                    raise KeyError(f"Cannot retrieve EdgeType.weight_config[{wkey}]['type'][{etype}]")

    # TODO: merge with method up
    @staticmethod
    def set_agent_type_weights(G):
        # Iterate edges
        for u, v, d in G.edges(data=True):
            length = d['Length']
            # Iterate weight keys
            for agentK in EdgeType.agent_keys:
                agent_weight = 0
                for wkey in EdgeType.weight_keys:
                    agent_weight_factor = EdgeType.weight_config[wkey]['agent_type'][agentK]
                    edge_type_factor = d[wkey]
                    agent_weight += edge_type_factor * agent_weight_factor * length
                G[u][v][agentK] = agent_weight
