"""Nearest-node lookup for coordinates on an OSM graph."""

from __future__ import annotations

import networkx as nx
import osmnx as ox


def nearest_node(G: nx.MultiDiGraph, lat: float, lon: float):
    """Return the OSM node id closest to a (lat, lon) point."""
    return ox.distance.nearest_nodes(G, X=lon, Y=lat)
