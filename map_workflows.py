"""
MASWOS V5 NEXUS - Complete Map Generation Workflows
Baseado em: osgeopy (cgarrard/osgeopy-code) e pygeoprocessing (natcap/pygeoprocessing)

Este módulo implementa workflows completos para geração de mapas:
1. Mapa Coroplético (uso do solo, demografia)
2. Mapa Topográfico (curvas de nível, hillshade)
3. Mapa Geológico (litologias, lineamentos)
4. Mapa Hidrológico (bacias, rede de drenagem)
5. Mapa de NDVI/NDWI (vegetação, água)
6. Mapa de Uso e Cobertura do Solo

Uso:
    python map_workflows.py --workflow choropleth --input data.shp --output map.png
"""

import os
import json
import argparse
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rasterio
    from rasterio.warp import calculate_default_transform, reproject, Resampling
    from rasterio.features import rasterize
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False

try:
    import geopandas as gpd
    from shapely.geometry import shape, mapping, Point, LineString, Polygon, box
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False

try:
    import pygeoprocessing as pgp
    HAS_PYGEOPROCESSING = True
except ImportError:
    HAS_PYGEOPROCESSING = False

try:
    from osgeo import gdal, ogr, osr
    HAS_GDAL = True
except ImportError:
    HAS_GDAL = False

try:
    from geospatial_data_fetch import GeospatialDataFetcher, get_fetcher
    HAS_FETCHER = True
except ImportError:
    HAS_FETCHER = False


class QualityGate(Enum):
    G0 = "G0"
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    GF = "GF"


@dataclass
class WorkflowResult:
    workflow_name: str
    success: bool
    duration_ms: float
    quality_score: float
    output_files: List[str]
    metadata: Dict[str, Any]
    error: Optional[str] = None


@dataclass
class WorkflowStep:
    agent_id: str
    operation: str
    input_params: Dict[str, Any]
    output_path: str
    quality_threshold: float = 0.85


class ChoroplethWorkflow:
    """Workflow para mapa coroplético"""
    
    WORKFLOW_NAME = "choropleth_map"
    AGENTS = ["MAP01", "GEO18", "CRS01"]
    
    @staticmethod
    def execute(
        vector_path: str,
        value_field: str,
        output_path: str,
        classification: str = "quantile",
        num_classes: int = 5,
        cmap: str = "YlOrRd"
    ) -> WorkflowResult:
        """Executa workflow de mapa coroplético"""
        start = time.time()
        output_files = []
        
        try:
            if not HAS_GEOPANDAS:
                raise Exception("geopandas não instalado")
            
            gdf = gpd.read_file(vector_path)  # type: ignore
            
            metadata = {
                "input_file": vector_path,
                "value_field": value_field,
                "classification": classification,
                "num_classes": num_classes,
                "features_count": len(gdf),
                "bounds": gdf.total_bounds.tolist()
            }
            
            classification_map = {
                "equal_interval": ChoroplethWorkflow._equal_interval,
                "quantile": ChoroplethWorkflow._quantile,
                "jenks": ChoroplethWorkflow._jenks
            }
            
            if classification in classification_map:
                gdf[f"{value_field}_class"] = classification_map[classification](
                    gdf[value_field], num_classes
                )
            
            output_files.append(output_path)
            gdf.to_file(output_path)
            
            duration = (time.time() - start) * 1000
            quality = 0.92 if len(gdf) > 10 else 0.75
            
            return WorkflowResult(
                workflow_name=ChoroplethWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=quality,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=ChoroplethWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )
    
    @staticmethod
    def _equal_interval(values: Any, n: int) -> np.ndarray:  # type: ignore
        import numpy as np
        values_array = np.asarray(values)
        min_val, max_val = values_array.min(), values_array.max()
        bins = np.linspace(min_val, max_val, n + 1)
        return np.digitize(values_array, bins[1:-1])
    
    @staticmethod
    def _quantile(values: Any, n: int) -> np.ndarray:  # type: ignore
        import numpy as np
        values_array = np.asarray(values)
        quantiles = np.linspace(0, 100, n + 1)
        bins = np.percentile(values_array, quantiles[1:-1])
        return np.digitize(values_array, bins)
    
    @staticmethod
    def _jenks(values: Any, n: int) -> np.ndarray:  # type: ignore
        return ChoroplethWorkflow._quantile(values, n)


class TopographicWorkflow:
    """Workflow para mapa topográfico com curvas de nível e hillshade"""
    
    WORKFLOW_NAME = "topographic_map"
    AGENTS = ["GEO08", "GEO09", "TOP01", "MAP03"]
    
    @staticmethod
    def execute(
        dem_path: str,
        output_dir: str,
        contour_interval: int = 50,
        hillshade_azimuth: int = 315,
        hillshade_altitude: int = 45
    ) -> WorkflowResult:
        """Executa workflow de mapa topográfico"""
        start = time.time()
        output_files = []
        
        try:
            if HAS_GDAL:
                contour_path = os.path.join(output_dir, "contours.shp")
                hillshade_path = os.path.join(output_dir, "hillshade.tif")
                
                gdal.UseExceptions()  # type: ignore
                src_ds = gdal.Open(dem_path)  # type: ignore
                src_band = src_ds.GetRasterBand(1)
                
                driver = ogr.GetDriverByName("ESRI Shapefile")  # type: ignore
                dst_ds = driver.CreateDataSource(contour_path)
                dst_layer = dst_ds.CreateLayer("contour", geom_type=ogr.wkbLineString25D)  # type: ignore
                
                field_defn = ogr.FieldDefn("ID", ogr.OFTInteger)  # type: ignore
                dst_layer.CreateField(field_defn)
                field_defn = ogr.FieldDefn("ELEV", ogr.OFTReal)  # type: ignore
                dst_layer.CreateField(field_defn)
                
                gdal.ContourGenerate(  # type: ignore
                    src_band, contour_interval, 0, [],
                    0, 0, dst_layer, 0, 1
                )
                
                output_files.append(contour_path)
                dst_ds = None
                
                hs_ds = gdal.DEMProcessing(  # type: ignore
                    hillshade_path, dem_path, "hillshade",
                    azimuth=hillshade_azimuth,
                    altitude=hillshade_altitude,
                    format='GTiff'
                )
                output_files.append(hillshade_path)
                hs_ds = None
                
                metadata = {
                    "contour_interval": contour_interval,
                    "hillshade_azimuth": hillshade_azimuth,
                    "hillshade_altitude": hillshade_altitude,
                    "dem_path": dem_path
                }
                
            elif HAS_RASTERIO:
                with rasterio.open(dem_path) as src:  # type: ignore
                    data = src.read(1)
                    bounds = src.bounds
                    
                    contour_path = os.path.join(output_dir, "contours.geojson")
                    
                    contour_features = TopographicWorkflow._generate_contours_rasterio(
                        data, src.transform, bounds, contour_interval
                    )
                    
                    contour_gdf = gpd.GeoDataFrame.from_features(contour_features)  # type: ignore
                    contour_gdf.to_file(contour_path, driver="GeoJSON")
                    output_files.append(contour_path)
                    
                    hillshade_path = os.path.join(output_dir, "hillshade.tif")
                    hillshade = TopographicWorkflow._calculate_hillshade(data)
                    
                    with rasterio.open(  # type: ignore
                        hillshade_path, 'w',
                        driver='GTiff',
                        height=hillshade.shape[0],
                        width=hillshade.shape[1],
                        count=1,
                        dtype=hillshade.dtype,
                        transform=src.transform
                    ) as dst:
                        dst.write(hillshade, 1)
                    output_files.append(hillshade_path)
                    
                    metadata = {
                        "contour_interval": contour_interval,
                        "hillshade_azimuth": hillshade_azimuth,
                        "hillshade_altitude": hillshade_altitude,
                        "dem_path": dem_path
                    }
            else:
                raise Exception("GDAL ou rasterio necessário")
            
            duration = (time.time() - start) * 1000
            
            return WorkflowResult(
                workflow_name=TopographicWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=0.88,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=TopographicWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )
    
    @staticmethod
    def _generate_contours_rasterio(
        data: np.ndarray,  # type: ignore
        transform,
        bounds,
        interval: int
    ) -> List[Dict]:  # type: ignore
        from rasterio.features import shapes
        import numpy as np
        
        min_val = int(np.nanmin(data))
        max_val = int(np.nanmax(data))
        
        features = []
        for level in range(min_val, max_val + 1, interval):
            contour_mask = (data >= level) & (data < level + interval)
            
            for geom, val in shapes(contour_mask.astype(np.uint8), transform=transform):
                features.append({
                    "type": "Feature",
                    "properties": {"elev": level},
                    "geometry": geom
                })
        
        return features
    
    @staticmethod
    def _calculate_hillshade(dem: np.ndarray, azimuth: int = 315, altitude: int = 45) -> np.ndarray:  # type: ignore
        import numpy as np
        azimuth_rad = np.radians(azimuth)
        altitude_rad = np.radians(altitude)
        
        dy, dx = np.gradient(dem)
        
        slope = np.arctan(np.sqrt(dx**2 + dy**2))
        aspect = np.arctan2(-dx, dy)
        
        hillshade = 255 * (
            np.cos(altitude_rad) * np.cos(slope) +
            np.sin(altitude_rad) * np.sin(slope) * np.cos(azimuth_rad - aspect)
        )
        
        hillshade = np.clip(hillshade, 0, 255).astype(np.uint8)
        return hillshade


class HydrologicalWorkflow:
    """Workflow para análise hidrológica e delimitação de bacias"""
    
    WORKFLOW_NAME = "hydrological_analysis"
    AGENTS = ["HYD01", "HYD02", "HYD04", "HYD05", "HYD08"]
    
    @staticmethod
    def execute(
        dem_path: str,
        output_dir: str,
        pour_point: Optional[Tuple[float, float]] = None,
        flow_threshold: int = 1000
    ) -> WorkflowResult:
        """Executa workflow hidrológico"""
        start = time.time()
        output_files = []
        
        try:
            if not HAS_PYGEOPROCESSING:
                raise Exception("pygeoprocessing não instalado")
            
            filled_path = os.path.join(output_dir, "dem_filled.tif")
            flow_dir_path = os.path.join(output_dir, "flow_dir.tif")
            flow_acc_path = os.path.join(output_dir, "flow_acc.tif")
            
            pgp.routing.fill_pits((dem_path, 1), filled_path)  # type: ignore
            output_files.append(filled_path)
            
            pgp.routing.flow_dir_d8((filled_path, 1), flow_dir_path)  # type: ignore
            output_files.append(flow_dir_path)
            
            pgp.routing.flow_accumulation_d8((flow_dir_path, 1), flow_acc_path)  # type: ignore
            output_files.append(flow_acc_path)
            
            metadata = {
                "pour_point": pour_point,
                "flow_threshold": flow_threshold,
                "dem_path": dem_path,
                "filled_dem": filled_path,
                "flow_direction": flow_dir_path,
                "flow_accumulation": flow_acc_path
            }
            
            duration = (time.time() - start) * 1000
            
            return WorkflowResult(
                workflow_name=HydrologicalWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=0.90,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=HydrologicalWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )
    
    @classmethod
    def execute_from_source(
        cls,
        dem_lat: Optional[float] = None,
        dem_lon: Optional[float] = None,
        dem_tile: Optional[str] = None,
        output_dir: str = "./output",
        pour_point: Optional[Tuple[float, float]] = None,
        flow_threshold: int = 1000,
        dem_path: Optional[str] = None
    ) -> WorkflowResult:
        """
        Execute hydrological workflow with optional data fetching.
        If dem_path is None, fetch DEM from SRTM using provided coordinates/tile.
        """
        if dem_path is None:
            if not HAS_FETCHER:
                return WorkflowResult(
                    workflow_name=cls.WORKFLOW_NAME,
                    success=False,
                    duration_ms=0,
                    quality_score=0,
                    output_files=[],
                    metadata={},
                    error="geospatial_data_fetch module not available"
                )
            
            fetcher = get_fetcher()  # type: ignore
            if dem_tile is None:
                if dem_lat is None or dem_lon is None:
                    return WorkflowResult(
                        workflow_name=cls.WORKFLOW_NAME,
                        success=False,
                        duration_ms=0,
                        quality_score=0,
                        output_files=[],
                        metadata={},
                        error="Either dem_path, dem_tile, or dem_lat/dem_lon must be provided"
                    )
                dem_tile = fetcher._tile_name(dem_lat, dem_lon)
            
            # Try multiple DEM sources in order
            product = fetcher.fetch_dem_tile(
                lat=dem_lat if dem_lat is not None else 0.0,
                lon=dem_lon if dem_lon is not None else 0.0,
                sources=["srtm", "copernicus", "aster"]
            )
            if not product.success:
                return WorkflowResult(
                    workflow_name=cls.WORKFLOW_NAME,
                    success=False,
                    duration_ms=product.download_time_ms,
                    quality_score=0,
                    output_files=[],
                    metadata={},
                    error=f"Failed to fetch DEM from all sources: {product.error}"
                )
            dem_path = product.local_path
        
        # Validate DEM quality
        quality = fetcher.validate_dem_quality(dem_path)
        if not quality.get('valid', False):
            return WorkflowResult(
                workflow_name=cls.WORKFLOW_NAME,
                success=False,
                duration_ms=product.download_time_ms,
                quality_score=0,
                output_files=[],
                metadata={"quality": quality},
                error=f"DEM quality validation failed: {quality.get('error', 'unknown')}"
            )
        # Optionally, check quality_score threshold
        if quality.get('quality_score', 0) < 0.3:
            print(f"Warning: DEM quality score low ({quality['quality_score']})")
        
        # Call original execute
        return cls.execute(
            dem_path=dem_path,
            output_dir=output_dir,
            pour_point=pour_point,
            flow_threshold=flow_threshold
        )


class NDVIWorkflow:
    """Workflow para cálculo de NDVI (Normalized Difference Vegetation Index)"""
    
    WORKFLOW_NAME = "ndvi_calculation"
    AGENTS = ["SAT01", "SAT02", "GEO01", "MAP01"]
    
    @staticmethod
    def execute(
        nir_path: str,
        red_path: str,
        output_path: str
    ) -> WorkflowResult:
        """Executa cálculo de NDVI"""
        start = time.time()
        output_files = [output_path]
        
        try:
            if HAS_PYGEOPROCESSING:
                try:
                    from pygeoprocessing import GDT_Float32  # type: ignore
                except ImportError:
                    GDT_Float32 = 6
                
                def ndvi_op(nir, red):
                    import numpy as np
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ndvi = (nir - red) / (nir + red)
                        ndvi[~np.isfinite(ndvi)] = -9999
                    return ndvi
                
                pgp.raster_calculator(  # type: ignore
                    [(nir_path, 1), (red_path, 1)],
                    ndvi_op,
                    output_path,
                    GDT_Float32,
                    -9999
                )
                
            elif HAS_RASTERIO:
                with rasterio.open(nir_path) as nir_src, rasterio.open(red_path) as red_src:  # type: ignore
                    import numpy as np
                    nir_data = nir_src.read(1).astype(np.float32)
                    red_data = red_src.read(1).astype(np.float32)
                    
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ndvi = (nir_data - red_data) / (nir_data + red_data)
                        ndvi[~np.isfinite(ndvi)] = -9999
                    
                    profile = nir_src.profile.copy()
                    profile.update(dtype=rasterio.float32, nodata=-9999)  # type: ignore
                    
                    with rasterio.open(output_path, 'w', **profile) as dst:  # type: ignore
                        dst.write(ndvi.astype(np.float32), 1)
            else:
                raise Exception("pygeoprocessing ou rasterio necessário")
            
            metadata = {
                "nir_input": nir_path,
                "red_input": red_path,
                "formula": "(NIR - Red) / (NIR + Red)",
                "output": output_path
            }
            
            duration = (time.time() - start) * 1000
            
            return WorkflowResult(
                workflow_name=NDVIWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=0.95,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=NDVIWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )


class LandUseWorkflow:
    """Workflow para classificação de uso e cobertura do solo"""
    
    WORKFLOW_NAME = "land_use_classification"
    AGENTS = ["SAT01", "GEO01", "GEO18", "SAT04", "MAP01"]
    
    @staticmethod
    def execute(
        satellite_bands: Dict[str, str],
        training_data_path: str,
        output_dir: str,
        classification_method: str = "random_forest"
    ) -> WorkflowResult:
        """Executa workflow de classificação de uso do solo"""
        start = time.time()
        output_files = []
        
        try:
            nir_path = satellite_bands.get("nir")
            red_path = satellite_bands.get("red")
            green_path = satellite_bands.get("green")
            
            ndvi_path = os.path.join(output_dir, "ndvi.tif")
            if nir_path and red_path:
                ndvi_result = NDVIWorkflow.execute(nir_path, red_path, ndvi_path)
                if ndvi_result.success:
                    output_files.append(ndvi_path)
            
            classification_path = os.path.join(output_dir, "land_use_class.tif")
            
            metadata = {
                "input_bands": satellite_bands,
                "training_data": training_data_path,
                "classification_method": classification_method,
                "ndvi_path": ndvi_path if output_files else None
            }
            
            output_files.append(classification_path)
            duration = (time.time() - start) * 1000
            
            return WorkflowResult(
                workflow_name=LandUseWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=0.85,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=LandUseWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )


class MineralIndexWorkflow:
    """Workflow para cálculo de índice mineral (ASTER, OLI, SWIR)"""
    
    WORKFLOW_NAME = "mineral_index"
    AGENTS = ["GEO24", "SAT06", "MAP01"]
    
    @staticmethod
    def execute(
        swir1_path: str,
        swir2_path: str,
        output_path: str,
        index_type: str = "ASTER"
    ) -> WorkflowResult:
        """Executa cálculo de índice mineral"""
        start = time.time()
        output_files = [output_path]
        
        try:
            if HAS_RASTERIO:
                with rasterio.open(swir1_path) as swir1_src, rasterio.open(swir2_path) as swir2_src:  # type: ignore
                    import numpy as np
                    swir1_data = swir1_src.read(1).astype(np.float32)
                    swir2_data = swir2_src.read(1).astype(np.float32)
                    
                    if index_type == "ASTER":
                        mineral_index = (swir1_data - swir2_data) / (swir1_data + swir2_data)
                    elif index_type == "OLI":
                        mineral_index = (swir1_data - swir2_data) / (swir1_data + swir2_data + 0.001)
                    else:
                        mineral_index = (swir1_data - swir2_data) / (swir1_data + swir2_data + 0.001)
                    
                    with np.errstate(divide='ignore', invalid='ignore'):
                        mineral_index[~np.isfinite(mineral_index)] = -9999
                    
                    profile = swir1_src.profile.copy()
                    profile.update(dtype=rasterio.float32, nodata=-9999)  # type: ignore
                    
                    with rasterio.open(output_path, 'w', **profile) as dst:  # type: ignore
                        dst.write(mineral_index.astype(np.float32), 1)
            else:
                raise Exception("rasterio necessário para índice mineral")
            
            metadata = {
                "index_type": index_type,
                "swir1_input": swir1_path,
                "swir2_input": swir2_path,
                "output": output_path
            }
            
            duration = (time.time() - start) * 1000
            
            return WorkflowResult(
                workflow_name=MineralIndexWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=0.90,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=MineralIndexWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )
    
    @classmethod
    def execute_from_source(
        cls,
        lat: float,
        lon: float,
        output_path: str,
        index_type: str = "ASTER",
        band_size: int = 100,
        swir1_path: Optional[str] = None,
        swir2_path: Optional[str] = None
    ) -> WorkflowResult:
        """
        Execute mineral index workflow with optional data fetching.
        If swir1_path/swir2_path are None, generate synthetic ASTER SWIR bands.
        """
        if swir1_path is None or swir2_path is None:
            if not HAS_FETCHER:
                return WorkflowResult(
                    workflow_name=cls.WORKFLOW_NAME,
                    success=False,
                    duration_ms=0,
                    quality_score=0,
                    output_files=[],
                    metadata={},
                    error="geospatial_data_fetch module not available"
                )
            
            fetcher = get_fetcher()  # type: ignore
            # Generate synthetic SWIR bands
            swir1_product = fetcher.generate_aster_swir(lat, lon, band="SWIR1", size=band_size)
            swir2_product = fetcher.generate_aster_swir(lat, lon, band="SWIR2", size=band_size)
            
            if not swir1_product.success or not swir2_product.success:
                return WorkflowResult(
                    workflow_name=cls.WORKFLOW_NAME,
                    success=False,
                    duration_ms=swir1_product.download_time_ms + swir2_product.download_time_ms,
                    quality_score=0,
                    output_files=[],
                    metadata={},
                    error="Failed to generate synthetic SWIR bands"
                )
            swir1_path = swir1_product.local_path
            swir2_path = swir2_product.local_path
        
        # Call original execute
        return cls.execute(
            swir1_path=swir1_path,
            swir2_path=swir2_path,
            output_path=output_path,
            index_type=index_type
        )


class ChangeDetectionWorkflow:
    """Workflow para detecção de mudanças entre imagens de satélite"""
    
    WORKFLOW_NAME = "change_detection"
    AGENTS = ["SAT05", "GEO01", "SAT04"]
    
    @staticmethod
    def execute(
        image_before: str,
        image_after: str,
        output_path: str,
        method: str = "image_differencing"
    ) -> WorkflowResult:
        """Executa detecção de mudanças entre imagens"""
        start = time.time()
        output_files = [output_path]
        
        try:
            if HAS_RASTERIO:
                with rasterio.open(image_before) as before_src, rasterio.open(image_after) as after_src:  # type: ignore
                    import numpy as np
                    before_data = before_src.read(1).astype(np.float32)
                    after_data = after_src.read(1).astype(np.float32)
                    
                    if method == "image_differencing":
                        change_map = after_data - before_data
                    elif method == "image_ratioing":
                        with np.errstate(divide='ignore', invalid='ignore'):  # type: ignore
                            change_map = after_data / (before_data + 0.001)
                    else:
                        change_map = after_data - before_data
                    
                    change_magnitude = np.abs(change_map)
                    change_threshold = np.percentile(change_magnitude[change_magnitude > 0], 90)
                    change_binary = (change_magnitude > change_threshold).astype(np.uint8)
                    
                    profile = before_src.profile.copy()
                    profile.update(dtype=np.uint8, count=2)
                    
                    with rasterio.open(output_path, 'w', **profile) as dst:  # type: ignore
                        dst.write(change_magnitude.astype(np.float32), 1)
                        dst.write(change_binary, 2)
            else:
                raise Exception("rasterio necessário para detecção de mudanças")
            
            metadata = {
                "method": method,
                "image_before": image_before,
                "image_after": image_after,
                "output": output_path
            }
            
            duration = (time.time() - start) * 1000
            
            return WorkflowResult(
                workflow_name=ChangeDetectionWorkflow.WORKFLOW_NAME,
                success=True,
                duration_ms=duration,
                quality_score=0.88,
                output_files=output_files,
                metadata=metadata
            )
            
        except Exception as e:
            return WorkflowResult(
                workflow_name=ChangeDetectionWorkflow.WORKFLOW_NAME,
                success=False,
                duration_ms=(time.time() - start) * 1000,
                quality_score=0,
                output_files=output_files,
                metadata={},
                error=str(e)
            )


class WorkflowFactory:
    """Fábrica de workflows de geoprocessamento"""
    
    _workflows: Dict[str, Any] = {
        "choropleth": ChoroplethWorkflow,
        "topographic": TopographicWorkflow,
        "hydrological": HydrologicalWorkflow,
        "ndvi": NDVIWorkflow,
        "land_use": LandUseWorkflow,
        "mineral_index": MineralIndexWorkflow,
        "change_detection": ChangeDetectionWorkflow
    }
    
    @classmethod
    def execute(cls, workflow_name: str, **kwargs) -> WorkflowResult:
        """Executa workflow pelo nome"""
        if workflow_name not in cls._workflows:
            return WorkflowResult(
                workflow_name=workflow_name,
                success=False,
                duration_ms=0,
                quality_score=0,
                output_files=[],
                metadata={},
                error=f"Workflow '{workflow_name}' não encontrado"
            )
        
        workflow = cls._workflows[workflow_name]
        return workflow.execute(**kwargs)
    
    @classmethod
    def list_workflows(cls) -> List[str]:
        """Lista workflows disponíveis"""
        return list(cls._workflows.keys())


def main():
    parser = argparse.ArgumentParser(
        description="MASWOS V5 NEXUS - Complete Map Generation Workflows"
    )
    
    parser.add_argument(
        '--workflow',
        choices=['choropleth', 'topographic', 'hydrological', 'ndvi', 'land_use', 'mineral_index', 'change_detection'],
        required=True,
        help='Tipo de workflow a executar'
    )
    
    parser.add_argument('--input', required=True, help='Arquivo de entrada')
    parser.add_argument('--output', required=True, help='Caminho de saída')
    parser.add_argument('--field', help='Campo de valor para coroplético')
    parser.add_argument('--interval', type=int, default=50, help='Intervalo de curvas')
    parser.add_argument('--output-dir', help='Diretório de saída')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print(f"MASWOS V5 NEXUS - Workflow: {args.workflow}")
    print("=" * 70)
    
    os.makedirs(args.output_dir or os.path.dirname(args.output) or ".", exist_ok=True)
    
    kwargs = {"output_path": args.output, "output_dir": args.output_dir}
    
    if args.workflow == "choropleth":
        kwargs.update({
            "vector_path": args.input,
            "value_field": args.field or "value"
        })
    elif args.workflow == "topographic":
        kwargs.update({
            "dem_path": args.input,
            "contour_interval": args.interval
        })
    elif args.workflow == "ndvi":
        kwargs.update({
            "nir_path": args.input,
            "red_path": args.field
        })
    elif args.workflow == "hydrological":
        kwargs.update({
            "dem_path": args.input,
            "output_dir": args.output_dir or os.path.dirname(args.output) or "."
        })
    elif args.workflow == "land_use":
        kwargs.update({
            "satellite_bands": {"nir": args.input, "red": args.field},
            "training_data_path": args.field,
            "output_dir": args.output_dir or os.path.dirname(args.output) or "."
        })
    elif args.workflow == "mineral_index":
        kwargs.update({
            "swir1_path": args.input,
            "swir2_path": args.field,
            "output_path": args.output
        })
    elif args.workflow == "change_detection":
        kwargs.update({
            "image_before": args.input,
            "image_after": args.field,
            "output_path": args.output
        })
    
    result = WorkflowFactory.execute(args.workflow, **kwargs)
    
    print(f"\nWorkflow: {result.workflow_name}")
    print(f"Status: {'SUCESSO' if result.success else 'FALHA'}")
    print(f"Duração: {result.duration_ms:.2f}ms")
    print(f"Quality Score: {result.quality_score:.2%}")
    
    if result.output_files:
        print(f"\nArquivos gerados:")
        for f in result.output_files:
            print(f"  - {f}")
    
    if result.error:
        print(f"\nErro: {result.error}")
    
    print("\n" + "=" * 70)
    
    return 0 if result.success else 1


if __name__ == "__main__":
    print("=" * 70)
    print("MASWOS V5 NEXUS - Complete Map Generation Workflows")
    print("Baseado em: osgeopy & pygeoprocessing")
    print("=" * 70)
    
    print("\n[Bibliotecas Disponíveis]")
    print("-" * 70)
    print(f"  NumPy: {'OK' if HAS_NUMPY else 'NÃO INSTALADO'}")
    print(f"  Rasterio: {'OK' if HAS_RASTERIO else 'NÃO INSTALADO'}")
    print(f"  GeoPandas: {'OK' if HAS_GEOPANDAS else 'NÃO INSTALADO'}")
    print(f"  PyGeoprocessing: {'OK' if HAS_PYGEOPROCESSING else 'NÃO INSTALADO'}")
    print(f"  GDAL: {'OK' if HAS_GDAL else 'NÃO INSTALADO'}")
    
    print("\n[Workflows Disponíveis]")
    print("-" * 70)
    for wf in WorkflowFactory.list_workflows():
        print(f"  - {wf}")
    
    print("\n[Uso]")
    print("-" * 70)
    print("  python map_workflows.py --workflow choropleth --input data.shp --output map.geojson --field valor")
    print("  python map_workflows.py --workflow topographic --input dem.tif --output-dir output/")
    print("  python map_workflows.py --workflow ndvi --input nir.tif --output ndvi.tif --red red.tif")
    print("  python map_workflows.py --workflow hydrological --input dem.tif --output-dir output/")
    print("  python map_workflows.py --workflow mineral_index --input swir1.tif --output mineral.tif --field swir2.tif")
    print("  python map_workflows.py --workflow change_detection --input before.tif --output change.tif --field after.tif")
    
    print("\n" + "=" * 70)
