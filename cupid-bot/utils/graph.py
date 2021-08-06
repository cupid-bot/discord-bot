"""Tool for drawing the family tree."""
import collections
import io

from cupid import RelationshipKind
from cupid.annotations import Graph, Relationship, User

import graphviz


def plot_nodes(graph: graphviz.Graph, users: dict[int, User]):
    """Add a node for each user on the graph."""
    for user in users.values():
        graph.node(str(user.id), user.name)


def force_same_rank(graph: graphviz.Graph, *users: User):
    """Ensure each of given user is displayed in the same vertical position."""
    subgraph = graphviz.Graph()
    subgraph.attr(rank='same')
    for user in users:
        subgraph.node(str(user.id))
    graph.subgraph(subgraph)


def plot_edges(graph: graphviz.Graph, relationships: list[Relationship]):
    """Add an edge between each related user to the graph."""
    # Map of parent ID -> children.
    siblings: dict[int, list[User]] = collections.defaultdict(list)
    for relationship in relationships:
        colour = (
            '#eb459e' if relationship.kind == RelationshipKind.MARRIAGE
            else '#404eed'
        )
        graph.edge(
            str(relationship.initiator.id),
            str(relationship.other.id),
            color=colour,
        )
        if relationship.kind == RelationshipKind.MARRIAGE:
            force_same_rank(graph, relationship.initiator, relationship.other)
        else:
            siblings[relationship.initiator.id].append(relationship.other)
    for children in siblings.values():
        force_same_rank(graph, *children)


def render_graph(data: Graph) -> io.BytesIO:
    """Draws the graph."""
    graph = graphviz.Graph(
        graph_attr={'bgcolor': '#36393f', 'splines': 'ortho'},
        node_attr={
            'shape': 'none',
            'fontcolor': '#ffffff',
            'fontname': 'Roboto,Helvetica,sans-serif',
        },
        edge_attr={'penwidth': '5'},
    )
    plot_nodes(graph, data.users)
    plot_edges(graph, data.relationships)
    stream = io.BytesIO(graph.pipe(format='png'))
    stream.seek(0)
    return stream
