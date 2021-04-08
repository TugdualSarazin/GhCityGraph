class EdgeType:
    # TODO: move to DEFAULT WEIGHT config
    weight_config = {
        'walk_time': {
            'type': {
                'commerce': 0,
                'intersection': 20,
                'office': 0,
                'park': 15,
                'residence': 0,
                'road': 15
            },
            'agent_type': {
                'Pedestrian': 8,
                'Car driver': 0,
            }
        },
        'drive_time': {
            'type': {
                'commerce': 0,
                'intersection': 10,
                'office': 0,
                'park': 10000,
                #'park': 1,
                'residence': 0,
                'road': 5
            },
            'agent_type': {
                'Pedestrian': 0,
                'Car driver': 10,
            }
        },
        'nature': {
            'type': {
                'commerce': 0,
                'intersection': 20,
                'office': 0,
                'park': 1,
                'residence': 0,
                'road': 20
            },
            'agent_type': {
                'Pedestrian': 40,
                'Car driver': 1,
            }
        }
    }

    weight_keys = set(weight_config)
    # agent_keys = {'Pedestrian', 'biker'}
    agent_keys = {'Pedestrian', 'Car driver'}
    edge_types = {'commerce', 'intersection', 'office', 'park', 'residence', 'road'}

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
            # Iterate weight keys
            for agentK in EdgeType.agent_keys:
                agent_weight = 0
                for wkey in EdgeType.weight_keys:
                    agent_weight_factor = EdgeType.weight_config[wkey]['agent_type'][agentK]
                    edge_type_factor = d[wkey]
                    agent_weight += edge_type_factor * agent_weight_factor
                G[u][v][agentK] = agent_weight
