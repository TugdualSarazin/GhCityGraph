import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import networkx as nx

from CityGraph.agent_path import AgentPath
from CityGraph.city_graph import CityGraph
from CityGraph.edge_type import EdgeType
import copy


class DrawConfig:
    def __init__(self, savefig=None, axis='on', node_color='grey', node_size=100, edge_size=3):
        self.savefig = savefig
        self.axis = axis

        # Graph config
        self.node_color = node_color
        self.node_size = node_size
        self.edge_size = edge_size

    def __copy__(self):
        self.__copy__()


class Drawer:
    def __init__(self, city_graph: CityGraph,
                 dpi=72, savefig=None, axis='on',
                 node_color='grey', node_size=100, edge_size=3):
        # Content config
        self.graph = city_graph

        # Matplotlib config
        self.dpi = dpi
        self.savefig = savefig
        self.axis = axis

        # Graph config
        self.node_color = node_color
        self.node_size = node_size
        self.edge_size = edge_size

    def draw(self, agent_paths):
        # Compute nb row
        nb_row = 2 + len(agent_paths) * 2
        # Compute nb cols
        nb_col = max(len(EdgeType.weight_keys), 2)

        # Set grid sepc
        fig = plt.figure(constrained_layout=True, dpi=self.dpi)
        gs = fig.add_gridspec(nb_row, nb_col)

        # Draw edge types row
        ax_graph_edge_type = fig.add_subplot(gs[0, :])
        self.graph_edge_type(ax_graph_edge_type)

        # Draw weights row
        self.draw_graphs_row(fig, gs, row=1)

        # Draw agent path rows
        axrow = 2
        for apath in agent_paths:
            ax_graph_agent_weight = fig.add_subplot(gs[axrow, 0])
            self.graph_edge_attr(ax_graph_agent_weight, apath.agent_type)
            # ax_graph_path = fig.add_subplot(gs[axrow, 1:])
            ax_graph_path = fig.add_subplot(gs[axrow, 1:])
            self.graph_agent_path(ax_graph_path, apath)
            axrow += 1
            ax_path_weight_plot = fig.add_subplot(gs[axrow, :])
            self.plot_agent_weight_path(ax_path_weight_plot, apath)
            axrow += 1

    def draw2(self, agent_paths):
        # Compute nb row
        nb_row = len(agent_paths) * 2
        # Compute nb cols
        nb_col = 2

        # Set grid sepc
        # fig = plt.figure(constrained_layout=True, dpi=self.dpi)
        fig = plt.figure(constrained_layout=True, figsize=(6, 8))
        gs = fig.add_gridspec(nb_row, nb_col, wspace=0., hspace=0.5, left=0.1, right=0.98, bottom=0.05, top=0.9)

        # Draw agent path rows
        axrow = 0
        for apath in agent_paths:
            ax_graph_agent_weight = fig.add_subplot(gs[axrow, 0])
            self.graph_edge_attr(ax_graph_agent_weight, apath.agent_type)
            # ax_graph_path = fig.add_subplot(gs[axrow, 1:])
            ax_graph_path = fig.add_subplot(gs[axrow, 1:])
            self.graph_agent_path(ax_graph_path, apath)
            axrow += 1
            ax_path_weight_plot = fig.add_subplot(gs[axrow, :])
            self.plot_agent_weight_path(ax_path_weight_plot, apath)
            axrow += 1

    def draw_weights(self):
        # Set grid spec
        nb_row = 1
        nb_col = 1
        fig = plt.figure(constrained_layout=True, figsize=(14, 8))
        gs = fig.add_gridspec(nb_row, nb_col, wspace=0., hspace=0., left=0., right=0.97, bottom=0.02, top=0.97)

        self.graphs_basic_weight(fig, gs[0:, 0])
        plt.savefig(f'../out/san_juan_weights.png', transparent=True)
        plt.show()

    def draw_static(self, agent_paths=[]):
        # self.draw(agent_paths)
        self.draw2(agent_paths)
        plt.show()

    def graphs_basic_weight(self, fig, gs_elem):
        # Init grid spec
        sqrt_elem = math.sqrt(len(EdgeType.weight_keys))
        nb_row = math.floor(sqrt_elem)+1
        nb_col = math.ceil(sqrt_elem)
        inner_gs = gridspec.GridSpecFromSubplotSpec(nb_row, nb_col, subplot_spec=gs_elem, wspace=0.08, hspace=0.2)
        cax = 0
        for attr in EdgeType.weight_keys:
            ax = fig.add_subplot(inner_gs[cax])
            self.graph_edge_attr(ax, attr)
            cax += 1

    def graphs_agent_weight(self, fig, gs_elem, agent_type):
        # Init grid spec
        nb_row = len(EdgeType.weight_keys) + 1
        # graph_col_size = 2
        graph_col_size = 1
        nb_col = graph_col_size * 2 + 1
        inner_gs = gridspec.GridSpecFromSubplotSpec(nb_row, nb_col, subplot_spec=gs_elem, wspace=0.05, hspace=0.3)

        # Draw title
        ax_title = fig.add_subplot(inner_gs[0, :])
        ax_title.text(0.5, 0, agent_type, fontsize=20, fontweight='bold')
        ax_title.axis('off')
        # Draw graphs and factor
        cax = 1
        for attr in EdgeType.weight_keys:
            # Retrieve factor
            factor = EdgeType.weight_config[attr]['agent_type'][agent_type]
            # Draw text factor
            ax_text_factor = fig.add_subplot(inner_gs[cax, 0])
            # ax_text_factor.text(0.5, 0.5, "{} \textbf{{x{}}}".format(attr, factor), fontsize=12, alpha=0.5)
            title = attr + r" $\bf{x" + str(factor) + "}$"
            ax_text_factor.text(0.5, 0.5, title, fontsize=12, alpha=0.5)
            ax_text_factor.axis('off')
            # Draw graph
            # ax_graph_factor = fig.add_subplot(inner_gs[cax, 1:graph_col_size])
            ax_graph_factor = fig.add_subplot(inner_gs[cax, 1])
            self.graph_edge_attr(ax_graph_factor, attr, factor=factor, display_tile=False)
            # Increment row index
            cax += 1

        # ax_graph_agent = fig.add_subplot(inner_gs[1:, graph_col_size+1:])
        ax_graph_agent = fig.add_subplot(inner_gs[1:, 2])
        self.graph_edge_attr(ax_graph_agent, agent_type, display_tile=False)

    def draw_agents_paths(self, edges_num, ax_edge_type, ax_map, ax_chart, apaths: [AgentPath]):
        ax_edge_type.clear()
        self.graph_edge_type(ax_edge_type)
        ax_map.clear()
        self.graph_agent_path(ax_map, apaths, edges_num)
        ax_chart.clear()
        self.plot_agent_weight_path(ax_chart, apaths, edges_num)

    def static_agents_paths(self, agents_path: [AgentPath], save_file=None):
        fig = plt.figure(constrained_layout=True, dpi=self.dpi)
        gs = fig.add_gridspec(3, 1)
        ax_edge_type = fig.add_subplot(gs[0, 0])
        ax_map = fig.add_subplot(gs[1, 0])
        ax_chart = fig.add_subplot(gs[2, 0])

        self.draw_agents_paths(None, ax_edge_type, ax_map, ax_chart, agents_path)
        plt.savefig(save_file, transparent=True)
        plt.show()

    def anime_agents_paths(self, agents_path: [AgentPath], save_file=None):
        import matplotlib;
        matplotlib.use("TkAgg")

        # Build plot
        fig = plt.figure(constrained_layout=True, dpi=self.dpi)
        gs = fig.add_gridspec(2, 1)
        ax_map = fig.add_subplot(gs[0, 0])
        ax_chart = fig.add_subplot(gs[1, 0])

        # Create a graph and layout
        max_edges_len = 0
        for apath in agents_path:
            edges_len = len(apath.path_edges)
            if edges_len > max_edges_len:
                max_edges_len = edges_len

        ani = animation.FuncAnimation(fig, self.draw_agents_paths, frames=max_edges_len, interval=200, repeat=False,
                                      fargs=(ax_map, ax_chart, agents_path))
        if save_file:
            ani.save(save_file, writer='imagemagick')

        plt.show()

    def draw_weight_path(self, edges_num, ax_map, ax_chart, agent_path: AgentPath, save_file):
        ax_map.clear()
        self.graph_agent_path(ax_map, [agent_path], edges_num)
        ax_chart.clear()
        self.plot_all_weight_path(ax_chart, agent_path, edges_num)
        plt.savefig(f'{save_file}-{edges_num}.png', transparent=True)

    def static_weight_path(self, agent_path: AgentPath, save_file=None):
        fig = plt.figure(constrained_layout=True, dpi=self.dpi)
        gs = fig.add_gridspec(2, 1)
        ax_map = fig.add_subplot(gs[0, 0])
        ax_chart = fig.add_subplot(gs[1, 0])

        self.draw_weight_path(None, ax_map, ax_chart, agent_path, save_file)
        plt.show()

    def anime_weight_path(self, agent_path: AgentPath, save_file=None):
        import matplotlib;
        matplotlib.use("TkAgg")

        # Build plot
        fig = plt.figure(constrained_layout=True, dpi=self.dpi)
        gs = fig.add_gridspec(2, 1)
        ax_map = fig.add_subplot(gs[0, 0])
        ax_chart = fig.add_subplot(gs[1, 0])

        # Create a graph and layout
        max_edges_len = len(agent_path.path_edges)

        ani = animation.FuncAnimation(fig, self.draw_weight_path, frames=max_edges_len, interval=200, repeat=False,
                                      fargs=(ax_map, ax_chart, agent_path, save_file))
        if save_file:
            ani.save(save_file, writer='imagemagick')

        plt.show()

    def plot_agent_weight_path(self, ax, agents_path: [AgentPath], edges_num=None):
        for apath in agents_path:
            if edges_num:
                path_edges = apath.path_edges[:edges_num]
            else:
                path_edges = apath.path_edges
            # attrs = list(EdgeType.weight_keys)
            attrs = []
            attrs.append(apath.agent_type)
            for attr in attrs:
                attr_values = [self.graph.G[u][v][attr] for u, v in path_edges]
                ax.plot(attr_values, label=attr, color=apath.color)
            ax.set_xlim([0, len(apath.path_edges)])

        # ax.legend(bbox_to_anchor=(1, 1), borderaxespad=0, frameon=False)
        ax.legend(loc='upper left')

    def plot_all_weight_path(self, ax, agent_path: AgentPath, edges_num=None):
        if edges_num:
            path_edges = agent_path.path_edges[:edges_num]
        else:
            path_edges = agent_path.path_edges
        for attr in EdgeType.weight_keys:
            agent_factor = EdgeType.weight_config[attr]['agent_type'][agent_path.agent_type]
            attr_values = [self.graph.G[u][v][attr] * agent_factor for u, v in path_edges]
            ax.plot(attr_values, label=attr)
        ax.set_xlim([0, len(agent_path.path_edges)])

        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        # ax.legend(loc='upper left')

    def graph_agent_path(self, ax, agents_path: [AgentPath], edges_num=None):
        for apath in agents_path:
            if edges_num:
                path_edges = apath.path_edges[:edges_num]
            else:
                path_edges = apath.path_edges
            nx.draw_networkx_edges(self.graph.G, self.graph.pos, ax=ax, edgelist=path_edges, edge_color=apath.color,
                                   width=self.edge_size + 1)
        nx.draw_networkx_edges(self.graph.G, self.graph.pos, ax=ax, alpha=0.2)
        nx.draw_networkx_nodes(self.graph.G, self.graph.pos, ax=ax, node_color=self.node_color,
                               node_size=self.node_size)

        # Draw color bar
        ax.axis(self.axis)
        # ax.set_title(f"Path (discomfort = {int(agent_path.weight)})")

    def draw_graphs_row(self, fig, gs, row):
        # Draw attributes graph values
        rax = 0
        for attr in EdgeType.weight_keys:
            ax = fig.add_subplot(gs[row, rax])
            self.graph_edge_attr(ax, attr, cmap=plt.cm.coolwarm)
            rax += 1

    def graph_edge_type(self, ax):
        nb_types = len(EdgeType.edge_types)
        cmap = plt.cm.get_cmap('tab10', nb_types)
        mapping_etype_color = {etype: color for etype, color in zip(EdgeType.edge_types, range(nb_types))}
        mapping_color_etype = {v: k for k, v in mapping_etype_color.items()}
        colors = [mapping_etype_color[etype] for etype in nx.get_edge_attributes(self.graph.G, 'type').values()]

        # Draw edges and nodes
        ec = nx.draw_networkx_edges(self.graph.G, self.graph.pos, ax=ax, width=self.edge_size,
                                    edge_color=colors, edge_cmap=cmap)
        nc = nx.draw_networkx_nodes(self.graph.G, self.graph.pos, ax=ax, node_color=self.node_color,
                                    node_size=self.node_size)

        formatter = plt.FuncFormatter(lambda val, loc: mapping_color_etype[val])
        plt.colorbar(ec, ax=ax, ticks=range(nb_types), format=formatter)
        ax.axis(self.axis)
        ax.set_title('Edge types')

    def graph_edge_attr(self, ax, attr, factor=1, display_tile=True, cmap=plt.cm.RdYlGn):
        # def graph_edge_attr(self, ax, attr, factor=1, display_tile=True, cmap=plt.cm.autumn.reversed()):
        # Extract attr values
        attr_values = [data.get(attr, 0) * factor for _, _, data in self.graph.G.edges(data=True)]
        # attr_values = [data.get(attr_key, 0) / data.get('length') for _, _, data in self.G.edges(data=True)]

        # Draw edges and nodes
        ec = nx.draw_networkx_edges(self.graph.G, self.graph.pos, ax=ax, width=self.edge_size,
                                    edge_color=attr_values, edge_cmap=cmap)
        nc = nx.draw_networkx_nodes(self.graph.G, self.graph.pos, ax=ax, node_color=self.node_color,
                                    node_size=self.node_size)

        # Draw color bar
        plt.colorbar(ec, ax=ax)
        ax.axis(self.axis)
        if display_tile:
            ax.set_title(attr)

    def graph_node_connection(self, ax):
        # Compute number of edges per node
        n_edges = [len(self.graph.G.edges(n)) for n in self.graph.G.nodes()]

        # Draw edges and nodes
        ec = nx.draw_networkx_edges(self.graph.G, self.graph.pos, ax=ax, alpha=0.2)
        nc = nx.draw_networkx_nodes(self.graph.G, self.graph.pos, ax=ax, node_size=self.node_size,
                                    node_color=n_edges, cmap=plt.cm.gnuplot)
        # Draw color bar
        plt.colorbar(nc, ax=ax)
        ax.axis(self.axis)
        ax.set_title('Nodes #edges')
