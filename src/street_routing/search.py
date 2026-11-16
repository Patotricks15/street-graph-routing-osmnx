"""Dijkstra and A* on a networkx multigraph with a length or time weight."""

from __future__ import annotations

import heapq
import itertools

import networkx as nx

from routes_pricing.geo import haversine_m


def _edge_weight(G: nx.MultiDiGraph, u, v, weight: str) -> float:
    """Smallest weight among parallel edges u->v, which is the one a router would take."""
    return min(data.get(weight, 0.0) for data in G[u][v].values())


def _node_latlon(G, node):
    return G.nodes[node]["y"], G.nodes[node]["x"]


def dijkstra(G: nx.MultiDiGraph, source, target, weight: str = "length"):
    """Return `(path, cost, nodes_expanded)` using Dijkstra's algorithm."""
    counter = itertools.count()
    dist = {source: 0.0}
    prev = {}
    frontier = [(0.0, next(counter), source)]
    settled = set()
    expanded = 0
    while frontier:
        cost, _, node = heapq.heappop(frontier)
        if node in settled:
            continue
        settled.add(node)
        expanded += 1
        if node == target:
            return _unwind(prev, source, target), cost, expanded
        for nbr in G.successors(node):
            new_cost = cost + _edge_weight(G, node, nbr, weight)
            if new_cost < dist.get(nbr, float("inf")):
                dist[nbr] = new_cost
                prev[nbr] = node
                heapq.heappush(frontier, (new_cost, next(counter), nbr))
    raise nx.NetworkXNoPath(f"No path from {source} to {target}")


def astar(G: nx.MultiDiGraph, source, target, weight: str = "length"):
    """Return `(path, cost, nodes_expanded)` using A* with a haversine heuristic.

    The heuristic is straight-line distance in metres. It is admissible only
    for `weight="length"`, because OSM edge lengths are never shorter than the
    great-circle distance between their endpoints.
    """
    if weight != "length":
        raise ValueError("The haversine heuristic is only admissible for weight='length'.")
    t_lat, t_lon = _node_latlon(G, target)

    def h(node):
        lat, lon = _node_latlon(G, node)
        return float(haversine_m(lat, lon, t_lat, t_lon))

    counter = itertools.count()
    g_cost = {source: 0.0}
    prev = {}
    frontier = [(h(source), next(counter), source)]
    settled = set()
    expanded = 0
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node in settled:
            continue
        settled.add(node)
        expanded += 1
        if node == target:
            return _unwind(prev, source, target), g_cost[target], expanded
        for nbr in G.successors(node):
            new_g = g_cost[node] + _edge_weight(G, node, nbr, weight)
            if new_g < g_cost.get(nbr, float("inf")):
                g_cost[nbr] = new_g
                prev[nbr] = node
                heapq.heappush(frontier, (new_g + h(nbr), next(counter), nbr))
    raise nx.NetworkXNoPath(f"No path from {source} to {target}")


def path_length(G: nx.MultiDiGraph, path, weight: str = "length") -> float:
    """Sum the weight along a node path."""
    return sum(_edge_weight(G, u, v, weight) for u, v in zip(path[:-1], path[1:]))


def _unwind(prev, source, target):
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return path[::-1]
