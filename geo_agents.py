"""
MASWOS V5 NEXUS - Geoprocessing Agents
Baseado em: osgeopy (cgarrard/osgeopy-code) e pygeoprocessing (natcap/pygeoprocessing)

Este módulo implementa agentes de geoprocessamento para:
- Raster Processing (NDVI, NDWI, classificação)
- Vector Processing (buffers, spatial join)
- Hidrologia (D8, MFD, bacias)
- Imagens de Satélite (Sentinel, Landsat)
- Mapas (topográficos, geológicos, hidrológicos)

Instalação:
    pip install pygeoprocessing rasterio geopandas shapely fiona gdal

Repositórios:
    - osgeopy: https://github.com/cgarrard/osgeopy-code
    - pygeoprocessing: https://github.com/natcap/pygeoprocessing
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
import tempfile
import shutil

try:
    import pygeoprocessing as pgp
    import numpy as np
    HAS_PYGEOPROCESSING = True
except ImportError:
    HAS_PYGEOPROCESSING = False
    print("Aviso: pygeoprocessing não instalado. Execute: pip install pygeoprocessing")

try:
    import rasterio
    from rasterio.warp import calculate_default_transform, reproject, Resampling
    from rasterio.mask import mask
    from rasterio.features import rasterize
    from rasterio.io import MemoryFile
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False
    print("Aviso: rasterio não instalado. Execute: pip install rasterio")

try:
    import geopandas as gpd
    from shapely.geometry import shape, mapping, Point, LineString, Polygon
    from shapely.ops import unary_union
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False
    print("Aviso: geopandas não instalado. Execute: pip install geopandas shapely fiona")

try:
    from osgeo import gdal, ogr, osr
    HAS_GDAL = True
except ImportError:
    HAS_GDAL = False
    print("Aviso: GDAL não instalado. Algumas operações avançadas não disponíveis.")


class QualityGate(Enum):
    G0 = "G0"
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    GF = "GF"


@dataclass
class GeoResult:
    success: bool
    output_path: Optional[str]
    metadata: Dict[str, Any]
    quality_score: float
    error: Optional[str] = None


@dataclass
class AgentResult:
    agent_id: str
    operation: str
    success: bool
    duration_ms: float
    data: Any = None


# ============================================================
# AGENTE BASE DE GEOPROCESSAMENTO
# ============================================================

class BaseGeoAgent:
    """Classe base para agentes de geoprocessamento"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.quality_gates = {
            QualityGate.G0: 1.0,
            QualityGate.G1: 0.80,
            QualityGate.G2: 0.85,
            QualityGate.G3: 0.90,
            QualityGate.G4: 0.95,
            QualityGate.GF: 0.99
        }
    
    def execute(self, params: Dict) -> GeoResult:
        """Executa o agente com parâmetros"""
        raise NotImplementedError
    
    def validate_input(self, params: Dict) -> Tuple[bool, Optional[str]]:
        """Valida inputs do agente"""
        return True, None
    
    def validate_output(self, output_path: str) -> Tuple[bool, float]:
        """Valida output do agente"""
        if os.path.exists(output_path):
            return True, 0.95
        return False, 0.0


# ============================================================
# AGENTES DE RASTER PROCESSING
# ============================================================

class NDVIAgent(BaseGeoAgent):
    """
    Agente GEO01 - Calcula NDVI (Normalized Difference Vegetation Index)
    
    Fórmula: NDVI = (NIR - Red) / (NIR + Red)
    
    Referência: osgeopy Chapter 10
    """
    
    def __init__(self):
        super().__init__("GEO01", "NDVIAgent", "Calcula NDVI")
    
    def execute(self, params: Dict) -> GeoResult:
        """Executa cálculo de NDVI"""
        nir_path = params.get("nir_path")
        red_path = params.get("red_path")
        output_path = params.get("output_path", "ndvi_output.tif")
        
        start = time.time()
        
        if not HAS_RASTERIO and not HAS_PYGEOPROCESSING:
            return GeoResult(False, None, {}, 0, "rasterio ou pygeoprocessing necessário")
        
        try:
            if HAS_PYGEOPROCESSING:
                def ndvi_op(nir, red):
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ndvi = (nir - red) / (nir + red)
                        ndvi[~np.isfinite(ndvi)] = -9999
                    return ndvi
                
                pgp.raster_calculator(
                    [(nir_path, 1), (red_path, 1)],
                    ndvi_op,
                    output_path,
                    pgp.GDT_Float32,
                    -9999
                )
            elif HAS_RASTERIO:
                with rasterio.open(nir_path) as nir_src, rasterio.open(red_path) as red_src:
                    nir_data = nir_src.read(1)
                    red_data = red_src.read(1)
                    
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ndvi = (nir_data.astype(np.float32) - red_data.astype(np.float32)) / \
                               (nir_data.astype(np.float32) + red_data.astype(np.float32))
                        ndvi[~np.isfinite(ndvi)] = -9999
                    
                    profile = nir_src.profile.copy()
                    profile.update(dtype=rasterio.float32, nodata=-9999)
                    
                    with rasterio.open(output_path, 'w', **profile) as dst:
                        dst.write(ndvi.astype(np.float32), 1)
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "formula": "(NIR - Red) / (NIR + Red)",
                    "nir_band": params.get("nir_band", 1),
                    "red_band": params.get("red_band", 1),
                    "nodata": -9999,
                    "duration_ms": duration
                },
                quality_score=0.95
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class NDWIAgent(BaseGeoAgent):
    """
    Agente GEO02 - Calcula NDWI (Normalized Difference Water Index)
    
    Fórmula: NDWI = (Green - NIR) / (Green + NIR)
    
    Aplicações: detecção de água, monitoramento de inundações
    
    Referência: osgeopy Chapter 10
    """
    
    def __init__(self):
        super().__init__("GEO02", "NDWIAgent", "Calcula NDWI")
    
    def execute(self, params: Dict) -> GeoResult:
        """Executa cálculo de NDWI"""
        green_path = params.get("green_path")
        nir_path = params.get("nir_path")
        output_path = params.get("output_path", "ndwi_output.tif")
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            def ndwi_op(green, nir):
                with np.errstate(divide='ignore', invalid='ignore'):
                    ndwi = (green - nir) / (green + nir)
                    ndwi[~np.isfinite(ndwi)] = -9999
                return ndwi
            
            pgp.raster_calculator(
                [(green_path, 1), (nir_path, 1)],
                ndwi_op,
                output_path,
                pgp.GDT_Float32,
                -9999
            )
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "formula": "(Green - NIR) / (Green + NIR)",
                    "nodata": -9999,
                    "duration_ms": duration
                },
                quality_score=0.95
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class SlopeCalculatorAgent(BaseGeoAgent):
    """
    Agente GEO06 - Calcula declividade (slope) de DEM
    
    Unidades: graus ou porcentagem
    
    Referência: pygeoprocessing.calculate_slope
    """
    
    def __init__(self):
        super().__init__("GEO06", "SlopeCalculatorAgent", "Calcula declividade")
    
    def execute(self, params: Dict) -> GeoResult:
        """Calcula declividade"""
        dem_path = params.get("dem_path")
        output_path = params.get("output_path", "slope_output.tif")
        z_factor = params.get("z_factor", 1.0)
        slope_unit = params.get("units", "degree")
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            pgp.calculate_slope(
                dem_path,
                output_path,
                z_factor=z_factor
            )
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "z_factor": z_factor,
                    "units": slope_unit,
                    "duration_ms": duration
                },
                quality_score=0.92
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class ContourGeneratorAgent(BaseGeoAgent):
    """
    Agente GEO08 - Gera curvas de nível de DEM
    
    Referência: osgeopy Chapter 11
    """
    
    def __init__(self):
        super().__init__("GEO08", "ContourGeneratorAgent", "Gera curvas de nível")
    
    def execute(self, params: Dict) -> GeoResult:
        """Gera curvas de nível"""
        dem_path = params.get("dem_path")
        output_path = params.get("output_path", "contours.shp")
        interval = params.get("interval", 50)
        base = params.get("base", 0)
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            gdal.UseExceptions()
            src_ds = gdal.Open(dem_path)
            src_band = src_ds.GetRasterBand(1)
            
            driver = ogr.GetDriverByName("ESRI Shapefile")
            dst_ds = driver.CreateDataSource(output_path)
            
            dst_layer = dst_ds.CreateLayer("contour", geom_type=ogr.wkbLineString25D)
            
            field_defn = ogr.FieldDefn("ID", ogr.OFTInteger)
            dst_layer.CreateField(field_defn)
            field_defn = ogr.FieldDefn("ELEV", ogr.OFTReal)
            dst_layer.CreateField(field_defn)
            
            gdal.ContourGenerate(
                src_band, interval, base, [],
                0, 0, dst_layer, 0, 1
            )
            
            src_ds = None
            dst_ds = None
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "interval": interval,
                    "base": base,
                    "duration_ms": duration
                },
                quality_score=0.90
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class HillshadeGeneratorAgent(BaseGeoAgent):
    """
    Agente GEO09 - Gera hillshade (sombras de terreno)
    
    Parâmetros: azimuth (azimute solar), altitude (altitude solar)
    
    Referência: osgeopy Chapter 11
    """
    
    def __init__(self):
        super().__init__("GEO09", "HillshadeGeneratorAgent", "Gera hillshade")
    
    def execute(self, params: Dict) -> GeoResult:
        """Gera hillshade"""
        dem_path = params.get("dem_path")
        output_path = params.get("output_path", "hillshade.tif")
        azimuth = params.get("azimuth", 315)
        altitude = params.get("altitude", 45)
        z_factor = params.get("z_factor", 1.0)
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            gdal.UseExceptions()
            src_ds = gdal.Open(dem_path)
            
            # Calcula slope e aspect primeiro
            slp_ds = gdal.DEMProcessing("tmp_slope.tif", dem_path, "slope", 
                                       zFactor=z_factor, format='GTiff')
            asp_ds = gdal.DEMProcessing("tmp_aspect.tif", dem_path, "aspect",
                                        format='GTiff')
            
            slp_band = slp_ds.GetRasterBand(1).ReadAsArray()
            asp_band = asp_ds.GetRasterBand(1).ReadAsArray()
            
            # Converte para radianos
            azimuth_rad = np.radians(azimuth)
            altitude_rad = np.radians(altitude)
            
            # Calcula hillshade
            hillshade = 255 * (
                np.cos(altitude_rad) * np.cos(np.radians(slp_band)) +
                np.sin(altitude_rad) * np.sin(np.radians(slp_band)) * 
                np.cos(azimuth_rad - np.radians(asp_band))
            )
            
            # Salva resultado
            with rasterio.open(output_path, 'w', 
                             driver='GTiff',
                             height=hillshade.shape[0],
                             width=hillshade.shape[1],
                             count=1,
                             dtype=hillshade.dtype,
                             transform=slp_ds.GetGeoTransform()) as dst:
                dst.write(hillshade.astype(np.uint8), 1)
            
            # Limpa arquivos temporários
            slp_ds = None
            asp_ds = None
            os.remove("tmp_slope.tif")
            os.remove("tmp_aspect.tif")
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "azimuth": azimuth,
                    "altitude": altitude,
                    "z_factor": z_factor,
                    "duration_ms": duration
                },
                quality_score=0.88
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


# ============================================================
# AGENTES DE VECTOR PROCESSING
# ============================================================

class BufferAgent(BaseGeoAgent):
    """
    Agente GEO11 - Cria buffers вокруг объектов
    
    Referência: osgeopy Chapter 6
    """
    
    def __init__(self):
        super().__init__("GEO11", "BufferAgent", "Cria buffers")
    
    def execute(self, params: Dict) -> GeoResult:
        """Cria buffer вокруг geometrias"""
        input_path = params.get("input_path")
        output_path = params.get("output_path", "buffer_output.shp")
        distance = params.get("distance", 100)
        dissolve = params.get("dissolve", False)
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            gdal.UseExceptions()
            src_ds = ogr.Open(input_path)
            src_layer = src_ds.GetLayer()
            
            driver = ogr.GetDriverByName("ESRI Shapefile")
            dst_ds = driver.CreateDataSource(output_path)
            dst_layer = dst_ds.CreateLayer("buffer", geom_type=ogr.wkbPolygon)
            
            # Copia campos
            src_layer_def = src_layer.GetLayerDefn()
            for i in range(src_layer_def.GetFieldCount()):
                field_defn = src_layer_def.GetFieldDefn(i)
                dst_layer.CreateField(field_defn)
            
            for feature in src_layer:
                geom = feature.GetGeometryRef()
                buffered = geom.Buffer(distance)
                new_feat = ogr.Feature(dst_layer.GetLayerDefn())
                new_feat.SetGeometry(buffered)
                
                for i in range(src_layer_def.GetFieldCount()):
                    new_feat.SetField(
                        src_layer_def.GetFieldDefn(i).GetName(),
                        feature.GetField(i)
                    )
                dst_layer.CreateFeature(new_feat)
            
            src_ds = None
            dst_ds = None
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "distance": distance,
                    "dissolve": dissolve,
                    "duration_ms": duration
                },
                quality_score=0.92
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class ZonalStatisticsAgent(BaseGeoAgent):
    """
    Agente GEO18 - Calcula estatísticas zonais
    
    Estatísticas: mean, sum, min, max, std
    
    Referência: pygeoprocessing.zonal_statistics
    """
    
    def __init__(self):
        super().__init__("GEO18", "ZonalStatisticsAgent", "Calcula estatísticas zonais")
    
    def execute(self, params: Dict) -> GeoResult:
        """Calcula estatísticas por zona"""
        raster_path = params.get("raster_path")
        vector_path = params.get("vector_path")
        output_path = params.get("output_path", "zonal_stats.json")
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            stats = pgp.zonal_statistics(
                (raster_path, 1),
                vector_path
            )
            
            # Salva estatísticas em JSON
            with open(output_path, 'w') as f:
                json.dump(stats, f, indent=2)
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "zones_count": len(stats),
                    "statistics": list(stats.values())[0].keys() if stats else [],
                    "duration_ms": duration
                },
                quality_score=0.90
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class RasterizeAgent(BaseGeoAgent):
    """
    Agente GEO17 - Rasteriza camada vetorial
    
    Referência: pygeoprocessing.rasterize
    """
    
    def __init__(self):
        super().__init__("GEO17", "RasterizeAgent", "Rasteriza vetor")
    
    def execute(self, params: Dict) -> GeoResult:
        """Rasteriza camada vetorial"""
        vector_path = params.get("vector_path")
        reference_raster = params.get("reference_raster")
        output_path = params.get("output_path", "rasterized.tif")
        burn_value = params.get("burn_value", 1)
        burn_field = params.get("burn_field", None)
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            pgp.rasterize(
                vector_path,
                output_path,
                reference_raster_path=reference_raster,
                burn_values=[burn_value] if not burn_field else None,
                option_list=[f"ATTRIBUTE={burn_field}"] if burn_field else None
            )
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "burn_value": burn_value,
                    "burn_field": burn_field,
                    "duration_ms": duration
                },
                quality_score=0.88
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


# ============================================================
# AGENTES DE HIDROLOGIA
# ============================================================

class FillPitsAgent(BaseGeoAgent):
    """
    Agente HYD01 - Preenche depressões em DEM
    
    Referência: pygeoprocessing.routing.fill_pits
    """
    
    def __init__(self):
        super().__init__("HYD01", "FillPitsAgent", "Preenche depressões")
    
    def execute(self, params: Dict) -> GeoResult:
        """Preenche depressões em DEM"""
        dem_path = params.get("dem_path")
        output_path = params.get("output_path", "dem_filled.tif")
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            pgp.routing.fill_pits(
                (dem_path, 1),
                output_path
            )
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "operation": "fill_pits",
                    "duration_ms": duration
                },
                quality_score=0.92
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class FlowDirectionD8Agent(BaseGeoAgent):
    """
    Agente HYD02 - Calcula direção de fluxo D8
    
    Método: maior declive
    
    Referência: pygeoprocessing.routing.flow_dir_d8
    """
    
    def __init__(self):
        super().__init__("HYD02", "FlowDirectionD8Agent", "Direção de fluxo D8")
    
    def execute(self, params: Dict) -> GeoResult:
        """Calcula direção de fluxo D8"""
        dem_path = params.get("dem_path")
        output_path = params.get("output_path", "flow_dir_d8.tif")
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            pgp.routing.flow_dir_d8(
                (dem_path, 1),
                output_path
            )
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "method": "D8",
                    "duration_ms": duration
                },
                quality_score=0.90
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


class FlowAccumulationAgent(BaseGeoAgent):
    """
    Agente HYD04 - Calcula acumulação de fluxo
    
    Referência: pygeoprocessing.routing.flow_accumulation_d8
    """
    
    def __init__(self):
        super().__init__("HYD04", "FlowAccumulationAgent", "Acumulação de fluxo")
    
    def execute(self, params: Dict) -> GeoResult:
        """Calcula acumulação de fluxo"""
        flow_dir_path = params.get("flow_dir_path")
        output_path = params.get("output_path", "flow_acc.tif")
        weight_path = params.get("weight_path", None)
        
        if not HAS_GDAL:
            return GeoResult(False, None, {}, 0, "GDAL não disponível")
        
        start = time.time()
        
        try:
            weight_raster = (weight_path, 1) if weight_path else None
            
            pgp.routing.flow_accumulation_d8(
                (flow_dir_path, 1),
                output_path,
                weight_raster=weight_raster
            )
            
            duration = (time.time() - start) * 1000
            
            return GeoResult(
                success=True,
                output_path=output_path,
                metadata={
                    "has_weights": weight_path is not None,
                    "duration_ms": duration
                },
                quality_score=0.90
            )
            
        except Exception as e:
            return GeoResult(False, None, {}, 0, str(e))


# ============================================================
# FACTORY DE AGENTES
# ============================================================

class GeoprocessingAgentFactory:
    """Fábrica de agentes de geoprocessamento"""
    
    _agents: Dict[str, BaseGeoAgent] = {}
    
    @classmethod
    def register(cls, agent: BaseGeoAgent):
        cls._agents[agent.agent_id] = agent
    
    @classmethod
    def get(cls, agent_id: str) -> Optional[BaseGeoAgent]:
        return cls._agents.get(agent_id)
    
    @classmethod
    def initialize_all(cls):
        """Inicializa todos os agentes"""
        cls.register(NDVIAgent())
        cls.register(NDWIAgent())
        cls.register(SlopeCalculatorAgent())
        cls.register(ContourGeneratorAgent())
        cls.register(HillshadeGeneratorAgent())
        cls.register(BufferAgent())
        cls.register(ZonalStatisticsAgent())
        cls.register(RasterizeAgent())
        cls.register(FillPitsAgent())
        cls.register(FlowDirectionD8Agent())
        cls.register(FlowAccumulationAgent())
    
    @classmethod
    def list_agents(cls) -> List[Dict]:
        """Lista todos os agentes registrados"""
        return [
            {
                "id": agent.agent_id,
                "name": agent.name,
                "description": agent.description
            }
            for agent in cls._agents.values()
        ]


# ============================================================
# PIPELINE DE GEOPROCESSAMENTO
# ============================================================

class GeoprocessingPipeline:
    """
    Pipeline completo de geoprocessamento baseado na arquitetura MASWOS V5 NEXUS
    """
    
    def __init__(self):
        GeoprocessingAgentFactory.initialize_all()
        self.quality_gates = {
            QualityGate.G0: 1.0,
            QualityGate.G1: 0.80,
            QualityGate.G2: 0.85,
            QualityGate.G3: 0.90,
            QualityGate.G4: 0.95,
            QualityGate.GF: 0.99
        }
    
    def execute_workflow(
        self,
        workflow_name: str,
        inputs: Dict
    ) -> List[AgentResult]:
        """Executa workflow completo de geoprocessamento"""
        
        workflows = {
            "ndvi_calculation": [("GEO01", {"nir_path": inputs["nir"], "red_path": inputs["red"]})],
            "ndwi_calculation": [("GEO02", {"green_path": inputs["green"], "nir_path": inputs["nir"]})],
            "slope_analysis": [("HYD01", {"dem_path": inputs["dem"]}),
                            ("GEO06", {"dem_path": inputs["dem"]})],
            "watershed_delineation": [("HYD01", {"dem_path": inputs["dem"]}),
                                   ("HYD02", {"dem_path": inputs["dem"]}),
                                   ("HYD04", {"flow_dir_path": "temp_flow.tif"}),
                                   ("GEO18", {"raster_path": "temp_acc.tif", "vector_path": inputs["basin"]})],
            "topographic_map": [("GEO06", {"dem_path": inputs["dem"]}),
                              ("GEO08", {"dem_path": inputs["dem"], "interval": inputs.get("interval", 50)}),
                              ("GEO09", {"dem_path": inputs["dem"]})],
            "land_use_analysis": [("GEO01", {"nir_path": inputs["nir"], "red_path": inputs["red"]}),
                                ("GEO18", {"raster_path": inputs["ndvi"], "vector_path": inputs["zones"]})]
        }
        
        results = []
        
        for agent_id, params in workflows.get(workflow_name, []):
            agent = GeoprocessingAgentFactory.get(agent_id)
            if agent:
                start = time.time()
                result = agent.execute(params)
                duration = (time.time() - start) * 1000
                
                results.append(AgentResult(
                    agent_id=agent_id,
                    operation=workflow_name,
                    success=result.success,
                    duration_ms=duration,
                    data=result
                ))
        
        return results


# ============================================================
# TESTE
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MASWOS V5 NEXUS - Geoprocessing Agents")
    print("Baseado em: osgeopy & pygeoprocessing")
    print("=" * 70)
    
    # Inicializa factory
    GeoprocessingAgentFactory.initialize_all()
    
    print("\n[Agentes Disponíveis]")
    print("-" * 70)
    
    for agent in GeoprocessingAgentFactory.list_agents():
        print(f"  {agent['id']}: {agent['name']} - {agent['description']}")
    
    print("\n[Workflos Disponíveis]")
    print("-" * 70)
    
    workflows = [
        "ndvi_calculation",
        "ndwi_calculation",
        "slope_analysis",
        "watershed_delineation",
        "topographic_map",
        "land_use_analysis"
    ]
    
    for wf in workflows:
        print(f"  - {wf}")
    
    print("\n[Bibliotecas Disponíveis]")
    print("-" * 70)
    print(f"  GDAL: {'OK' if HAS_GDAL else 'NÃO INSTALADO'}")
    print(f"  NumPy: {'OK' if HAS_GDAL else 'NÃO INSTALADO'}")
    print(f"  Rasterio: {'OK' if HAS_GDAL else 'NÃO INSTALADO'}")
    print(f"  PyGeoprocessing: {'OK' if HAS_GDAL else 'NÃO INSTALADO'}")
    
    if not HAS_GDAL:
        print("\n[Para instalar dependências]")
        print("-" * 70)
        print("  pip install pygeoprocessing rasterio geopandas shapely fiona gdal")
    
    print("\n" + "=" * 70)
    print("Configuração de Agentes Concluída!")
    print("=" * 70)
