# Data

No raw data is committed. Every file under `data/` except this README is git-ignored.

## Source

- **Graph:** OpenStreetMap drive network, "Manhattan, New York City, New York, USA", via `osmnx` 2.0.7 and the Overpass API.
- **Licence:** ODbL (OpenStreetMap contributors).
- **Retrieved:** 2026-11-16, through the Overpass endpoint `overpass.osm.ch` after the default endpoint returned "at capacity" responses.
- **Cache:** `$UBER_DATA_DIR/cache/manhattan_drive.graphml` (7 MB). Set `UBER_DATA_DIR` to a folder outside the repo. Without it, the notebook reads `../data`.

## Reproduce

The first run queries Overpass. Overpass sometimes refuses requests, so retry with backoff. Later runs load the GraphML file and need no network.
