import sys
sys.path.insert(0, '.')

from geospatial_data_fetch import GeospatialDataFetcher

fetcher = GeospatialDataFetcher()
# Test tile S22W043
product = fetcher.download_srtm_tile(lat=-22.9, lon=-43.2, tile_name="S22W043")
print(f"Success: {product.success}")
print(f"Error: {product.error}")
print(f"Metadata: {product.metadata}")
print(f"Local path: {product.local_path}")

# Test synthetic ASTER
product2 = fetcher.generate_aster_swir(lat=-22.9, lon=-43.2, band="SWIR1")
print(f"Synthetic success: {product2.success}")
print(f"Synthetic path: {product2.local_path}")

# Test ANA stations
stations = fetcher.fetch_ana_stations(state="SP", limit=3)
print(f"Stations found: {len(stations)}")
for st in stations:
    print(st)