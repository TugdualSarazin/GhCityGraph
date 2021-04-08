from flask import Flask
import ghhops_server as hs
import networkx as nx
from rhino3dm import Curve

from rhino3dm._rhino3dm import Point, Point3d, Polyline, LineCurve, Line

from CityGraph.city_graph import CityGraph
from CityGraph.edge_type_opti import EdgeType
from CityGraph.graph_tool import print_edges, print_nodes

app = Flask(__name__)
hops = hs.Hops(app)


def p3d_to_tuple(p: Point3d):
    return (p.X, p.Y, p.Z)


def init_graph(edges: [Curve], edges_types: [str]):
    G = nx.Graph()
    for e, etype in zip(edges, edges_types):
        G.add_edge(p3d_to_tuple(e.From), p3d_to_tuple(e.To), type=etype, length=e.Length)
    return G


def extract_types(G):
    return list(nx.get_edge_attributes(G, 'type').values())


@hops.component(
    "/lines_14",
    name="Lines",
    inputs=[
        hs.HopsCurve("Edges", "E", access=hs.HopsParamAccess.LIST),
        hs.HopsString("EdgesTypes", "ET", access=hs.HopsParamAccess.LIST),
        hs.HopsPoint("AgentsCoordinates", "AC", access=hs.HopsParamAccess.LIST),
        hs.HopsString("AgentsTypes", "AT", access=hs.HopsParamAccess.LIST),
        hs.HopsNumber("Updater", "u"),
    ],
    outputs=[
        hs.HopsString("NewTypes", "NT", access=hs.HopsParamAccess.LIST)
    ]
)
def lines(edges: [Curve], edges_types: [str],
          agents_coordinates: [Point3d], agents_types: [str],
          _):
    G = init_graph(edges, edges_types)
    EdgeType.set_weight(G)
    city_graph = CityGraph(G, geo_graph=False)
    print_edges(G)
    print_nodes(G)
    return extract_types(G)


if __name__ == "__main__":
    app.run()
