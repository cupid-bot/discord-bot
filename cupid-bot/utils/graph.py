"""Tool for drawing the family tree."""
import io

from cupid import RelationshipKind
from cupid.annotations import Graph, Relationship, User

import graphviz


def plot_nodes(graph: graphviz.Graph, users: dict[int, User]):
    """Add a node for each user on the graph."""
    for user in users.values():
        graph.node(str(user.id), user.name)


def plot_edges(graph: graphviz.Graph, relationships: list[Relationship]):
    """Add an edge between each related user to the graph."""
    for relationship in relationships:
        graph.edge(
            str(relationship.initiator.id),
            str(relationship.other.id),
            color='#eb459e' if relationship.kind == RelationshipKind.MARRIAGE else '#404eed',
        )
        if relationship.kind == RelationshipKind.MARRIAGE:
            subgraph = graphviz.Graph()
            subgraph.attr(rank='same')
            subgraph.node(str(relationship.initiator.id))
            subgraph.node(str(relationship.other.id))
            graph.subgraph(subgraph)


def render_graph(data: Graph) -> io.BytesIO:
    """Draws the graph."""
    graph = graphviz.Graph(
        graph_attr={
            'bgcolor': '#36393f',
            'splines': 'ortho',
        },
        node_attr={
            'shape': 'none',
            'fontcolor': '#ffffff',
            'fontname': 'Roboto,Helvetica,sans-serif',
        },
        edge_attr={
            'penwidth': '5',
        },
    )
    plot_nodes(graph, data.users)
    plot_edges(graph, data.relationships)
    stream = io.BytesIO(graph.pipe(format='png'))
    stream.seek(0)
    return stream
