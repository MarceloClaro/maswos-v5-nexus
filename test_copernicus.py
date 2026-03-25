import sys
sys.path.insert(0, '.')

from geospatial_data_fetch import GeospatialDataFetcher

fetcher = GeospatialDataFetcher()
# Test tile N00E006 (should exist)
product = fetcher.download_copernicus_tile(lat=0.5, lon=6.5, tile_name="N00E006")
print(f"Copernicus download: {product.success}")
if product.success:
    print(f"Path: {product.local_path}")
    print(f"Size: {product.metadata.get('size_bytes', 0)} bytes")
else:
    print(f"Error: {product.error}")
    # Try with tile name from lat/lon
    product2 = fetcher.download_copernicus_tile(lat=0.5, lon=6.5)
    print(f"Second attempt: {product2.success}")