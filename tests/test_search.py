import networkx as nx
import pytest

from street_routing.search import astar, dijkstra, path_length


def _toy_graph():
    """A small grid with coordinates so the haversine heuristic is meaningful."""
    G = nx.MultiDiGraph()
    coords = {
        "a": (40.7500, -73.9900),
        "b": (40.7510, -73.9900),
        "c": (40.7500, -73.9880),
        "d": (40.7510, -73.9880),
        "e": (40.7520, -73.9890),
    }
    for node, (lat, lon) in coords.items():
        G.add_node(node, y=lat, x=lon)
    edges = [("a", "b", 120.0), ("a", "c", 150.0), ("b", "d", 140.0), ("c", "d", 110.0),
             ("b", "e", 90.0), ("e", "d", 95.0), ("d", "e", 500.0)]
    for u, v, length in edges:
        G.add_edge(u, v, length=length)
        G.add_edge(v, u, length=length)
    return G


def test_dijkstra_and_astar_return_the_same_optimal_cost():
    G = _toy_graph()
    _, d_cost, _ = dijkstra(G, "a", "d")
    _, a_cost, _ = astar(G, "a", "d")
    assert d_cost == pytest.approx(a_cost)
    assert d_cost == pytest.approx(nx.dijkstra_path_length(G, "a", "d", weight="length"))


def test_returned_path_is_valid_and_sums_to_cost():
    G = _toy_graph()
    path, cost, _ = astar(G, "a", "d")
    assert path[0] == "a" and path[-1] == "d"
    assert path_length(G, path) == pytest.approx(cost)


def test_astar_rejects_time_weights():
    with pytest.raises(ValueError):
        astar(_toy_graph(), "a", "d", weight="travel_time")
