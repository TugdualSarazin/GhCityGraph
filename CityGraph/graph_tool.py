import networkx as nx


def load_graph(shp_path):
    G = nx.read_shp(shp_path, simplify=False, geom_attrs=False)
    return G.to_undirected()


def find_edge_by_attr(G, name, value):
    for u, v, attrs in G.edges(data=True):
        if attrs.get(name) == value:
            return u, v
    return None


def find_node_by_edge_type(G, edge_type):
    return [u for (u, v), t in nx.get_edge_attributes(G, 'type').items() if t == edge_type]


# TODO: need a unit test
def path_nodes_to_edges(path_nodes):
    prev_node = None
    edges = []
    for n in path_nodes:
        if prev_node is not None:
            edges.append((prev_node, n))
        prev_node = n

    return edges


def print_nodes(G):
    print('## Nodes ##')
    for n in G.nodes(data=True):
        print(n)


def print_edges(G):
    print('## Edges ##')
    for u, v, d in G.edges(data=True):
        print(u, v, d)
