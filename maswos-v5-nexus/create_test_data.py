"""
MASWOS V5 NEXUS - Test Data Generator
Creates sample geospatial data for testing workflows
"""

import os
import numpy as np

try:
    import rasterio
    from rasterio.transform import from_bounds
except ImportError:
    rasterio = None

try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon, box
except ImportError:
    gpd = None

def create_sample_vector_data(output_path: str) -> bool:
    """Creates sample vector data for choropleth map testing"""
    if gpd is None:
        print("GeoPandas not available")
        return False
    
    try:
        polygons = [
            {
                'id': 1,
                'name': 'Região Norte',
                'population': 1800000,
                'density': 3.5,
                'geometry': box(-45, -2, -38, 3)
            },
            {
                'id': 2,
                'name': 'Região Sul',
                'population': 2800000,
                'density': 8.2,
                'geometry': box(-42, -8, -38, -5)
            },
            {
                'id': 3,
                'name': 'Região Leste',
                'population': 1500000,
                'density': 12.5,
                'geometry': box(-38, -5, -35, -2)
            },
            {
                'id': 4,
                'name': 'Região Oeste',
                'population': 900000,
                'density': 2.1,
                'geometry': box(-48, -5, -45, -2)
            }
        ]
        
        gdf = gpd.GeoDataFrame(polygons, crs="EPSG:4326")
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        gdf.to_file(output_path)
        print(f"Created vector data: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating vector data: {e}")
        return False


def create_sample_dem(output_path: str, width: int = 100, height: int = 100) -> bool:
    """Creates sample DEM (Digital Elevation Model) for topographic testing"""
    if rasterio is None:
        print("Rasterio not available")
        return False
    
    try:
        bounds = (-45, -5, -35, 5)
        transform = from_bounds(*bounds, width, height)
        
        x = np.linspace(bounds[0], bounds[2], width)
        y = np.linspace(bounds[1], bounds[3], height)
        xx, yy = np.meshgrid(x, y)
        
        dem = (
            500 + 
            200 * np.sin(xx * 0.1) * np.cos(yy * 0.1) +
            100 * np.random.random((height, width))
        )
        
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=dem.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(dem, 1)
        
        print(f"Created DEM: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating DEM: {e}")
        return False


def create_sample_ndvi_bands(output_dir: str) -> dict:
    """Creates sample NIR and RED bands for NDVI calculation"""
    if rasterio is None:
        return {}
    
    try:
        width, height = 100, 100
        bounds = (-45, -5, -35, 5)
        transform = from_bounds(*bounds, width, height)
        
        x = np.linspace(bounds[0], bounds[2], width)
        y = np.linspace(bounds[1], bounds[3], height)
        xx, yy = np.meshgrid(x, y)
        
        vegetation = (np.sin(xx * 0.2) * np.cos(yy * 0.2) + 1) / 2
        
        nir = (0.5 + vegetation * 0.4 + np.random.random((height, width)) * 0.1).astype(np.float32)
        red = (0.3 - vegetation * 0.2 + np.random.random((height, width)) * 0.1).astype(np.float32)
        
        nir_path = os.path.join(output_dir, "sample_nir.tif")
        red_path = os.path.join(output_dir, "sample_red.tif")
        
        os.makedirs(output_dir, exist_ok=True)
        
        profile = {
            'driver': 'GTiff',
            'height': height,
            'width': width,
            'count': 1,
            'dtype': 'float32',
            'crs': 'EPSG:4326',
            'transform': transform
        }
        
        with rasterio.open(nir_path, 'w', **profile) as dst:
            dst.write(nir, 1)
        
        with rasterio.open(red_path, 'w', **profile) as dst:
            dst.write(red, 1)
        
        print(f"Created NIR band: {nir_path}")
        print(f"Created RED band: {red_path}")
        
        return {'nir': nir_path, 'red': red_path}
        
    except Exception as e:
        print(f"Error creating NDVI bands: {e}")
        return {}


def main():
    print("=" * 70)
    print("MASWOS V5 NEXUS - Test Data Generator")
    print("=" * 70)
    
    test_dir = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(test_dir, exist_ok=True)
    
    print("\n[1] Creating sample vector data for choropleth map...")
    vector_path = os.path.join(test_dir, "regions.shp")
    create_sample_vector_data(vector_path)
    
    print("\n[2] Creating sample DEM for topographic map...")
    dem_path = os.path.join(test_dir, "sample_dem.tif")
    create_sample_dem(dem_path)
    
    print("\n[3] Creating sample NIR/RED bands for NDVI calculation...")
    ndvi_bands = create_sample_ndvi_bands(test_dir)
    
    print("\n" + "=" * 70)
    print("Test data created successfully!")
    print(f"Location: {test_dir}")
    print("=" * 70)
    
    if ndvi_bands:
        print("\n[Testing NDVI workflow...]")
        from map_workflows import WorkflowFactory
        
        result = WorkflowFactory.execute(
            "ndvi",
            nir_path=ndvi_bands['nir'],
            red_path=ndvi_bands['red'],
            output_path=os.path.join(test_dir, "ndvi_result.tif")
        )
        
        print(f"\nNDVI Workflow Result:")
        print(f"  Success: {result.success}")
        print(f"  Duration: {result.duration_ms:.2f}ms")
        print(f"  Quality Score: {result.quality_score:.2%}")
        if result.output_files:
            print(f"  Output: {result.output_files[0]}")
    
    if os.path.exists(vector_path):
        print("\n[Testing Choropleth workflow...]")
        from map_workflows import WorkflowFactory
        
        result = WorkflowFactory.execute(
            "choropleth",
            vector_path=vector_path,
            value_field="population",
            output_path=os.path.join(test_dir, "choropleth_result.geojson")
        )
        
        print(f"\nChoropleth Workflow Result:")
        print(f"  Success: {result.success}")
        print(f"  Duration: {result.duration_ms:.2f}ms")
        print(f"  Quality Score: {result.quality_score:.2%}")
        if result.output_files:
            print(f"  Output: {result.output_files[0]}")
    
    print("\n" + "=" * 70)
    return 0


if __name__ == "__main__":
    main()
