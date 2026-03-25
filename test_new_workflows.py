import sys
sys.path.insert(0, '.')

from map_workflows import HydrologicalWorkflow, MineralIndexWorkflow
import os

os.makedirs("./test_output", exist_ok=True)

print("Testing HydrologicalWorkflow.execute_from_source...")
# Try to fetch DEM for a tile that may not exist; expect failure but handle gracefully
result = HydrologicalWorkflow.execute_from_source(
    dem_lat=-22.9,
    dem_lon=-43.2,
    output_dir="./test_output",
    flow_threshold=500
)
print(f"Hydrological result: {result.success}")
print(f"Error: {result.error}")
print(f"Duration: {result.duration_ms:.2f}ms")

# Use a synthetic DEM created by create_test_data
dem_path = "./test_data/sample_dem.tif"
if os.path.exists(dem_path):
    result = HydrologicalWorkflow.execute(
        dem_path=dem_path,
        output_dir="./test_output",
        flow_threshold=500
    )
    print(f"Hydrological with existing DEM: {result.success}")
    if not result.success:
        print(f"Error: {result.error}")
    print(f"Output files: {result.output_files}")

print("\nTesting MineralIndexWorkflow.execute_from_source...")
# This should generate synthetic SWIR bands
result = MineralIndexWorkflow.execute_from_source(
    lat=-22.9,
    lon=-43.2,
    output_path="./test_output/mineral_index.tif",
    band_size=50
)
print(f"Mineral index result: {result.success}")
print(f"Error: {result.error}")
print(f"Output files: {result.output_files}")
if result.success and result.output_files:
    for f in result.output_files:
        print(f"  - {f} (exists: {os.path.exists(f)})")

print("\nAll tests completed.")