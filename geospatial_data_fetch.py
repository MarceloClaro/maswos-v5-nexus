"""
MASWOS V5 NEXUS - Geospatial Data Fetcher
Downloads real hydrological and mineral data from public APIs
"""

import os
import math
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import warnings

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    warnings.warn("requests library not installed. Data fetching will be limited.")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rasterio
    from rasterio.transform import from_bounds
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False


@dataclass
class DataProduct:
    """Represents a downloaded geospatial data product"""
    name: str
    source: str
    format: str
    local_path: str
    metadata: Dict[str, Any]
    download_time_ms: float
    success: bool
    error: Optional[str] = None


class GeospatialDataFetcher:
    """
    Fetcher for real hydrological and mineral data from public APIs.
    Supports:
    - SRTM 30m DEM tiles from USGS
    - ANA precipitation data (HidroWeb)
    - ASTER SWIR bands (simulated)
    """
    
    # SRTM tile server (public, no authentication required)
    SRTM_BASE_URL = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"
    
    # Copernicus DEM tile server (public, no authentication required)
    COPERNICUS_BASE_URL = "https://copernicus-dem-30m.s3.amazonaws.com"
    
    # NASA Earthdata ASTER GDEM (requires authentication)
    ASTER_GDEM_BASE_URL = "https://e4ftl01.cr.usgs.gov/ASTT/ASTGTM.003/2000.01.01"
    # CMR API for searching granules
    CMR_SEARCH_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"
    
    # ANA HidroWeb API (public) - new endpoint
    ANA_HIDROWEB_BASE = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx"
    
    def __init__(self, cache_dir: str = "./geospatial_cache", 
                 earthdata_user: Optional[str] = None, 
                 earthdata_pass: Optional[str] = None):
        self.cache_dir = cache_dir
        self.earthdata_user = earthdata_user
        self.earthdata_pass = earthdata_pass
        self._earthdata_session = None
        os.makedirs(cache_dir, exist_ok=True)
        self.session = None
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'MASWOS-V5-NEXUS/1.0 (geospatial fetcher)'
            })
    
    def _get_earthdata_session(self):
        """Get or create authenticated session for NASA Earthdata"""
        if self._earthdata_session is not None:
            return self._earthdata_session
        
        if not HAS_REQUESTS:
            return None
        
        if self.earthdata_user is None or self.earthdata_pass is None:
            # Try to get from environment variables
            self.earthdata_user = os.environ.get('EARTHDATA_USER')
            self.earthdata_pass = os.environ.get('EARTHDATA_PASS')
            if self.earthdata_user is None or self.earthdata_pass is None:
                print("Warning: Earthdata credentials not provided. Set EARTHDATA_USER and EARTHDATA_PASS environment variables.")
                return None
        
        # Create session with authentication
        session = requests.Session()
        session.auth = (self.earthdata_user, self.earthdata_pass)
        # Pre-authenticate to NASA Earthdata login
        try:
            # First request to get cookies
            auth_url = "https://urs.earthdata.nasa.gov/"
            response = session.get(auth_url, timeout=30)
            if response.status_code == 200:
                self._earthdata_session = session
                return session
        except Exception as e:
            print(f"Earthdata authentication failed: {e}")
        return None
    
    def _tile_name(self, lat: float, lon: float) -> str:
        """
        Convert lat/lon to SRTM tile name.
        Example: lat=-22.5, lon=-43.2 -> S22W043
        """
        lat_int = int(math.floor(abs(lat)))
        lon_int = int(math.floor(abs(lon)))
        lat_prefix = 'N' if lat >= 0 else 'S'
        lon_prefix = 'E' if lon >= 0 else 'W'
        return f"{lat_prefix}{lat_int:02d}{lon_prefix}{lon_int:03d}"
    
    def _copernicus_tile_path(self, tile_name: str) -> str:
        """
        Convert tile name (e.g., S22W043) to Copernicus DEM path.
        Returns folder and file name.
        """
        # tile_name format: [NS]{2 digit lat}[EW]{3 digit lon}
        # Example: S22W043 -> Copernicus_DSM_COG_10_S22_00_W043_00_DEM/Copernicus_DSM_COG_10_S22_00_W043_00_DEM.tif
        lat_prefix = tile_name[0]
        lat_num = tile_name[1:3]
        lon_prefix = tile_name[3]
        lon_num = tile_name[4:7]
        folder = f"Copernicus_DSM_COG_10_{lat_prefix}{lat_num}_00_{lon_prefix}{lon_num}_00_DEM"
        file = f"{folder}.tif"
        return f"{folder}/{file}"
    
    def download_srtm_tile(self, lat: float, lon: float, tile_name: Optional[str] = None) -> DataProduct:
        """
        Download SRTM 30m DEM tile for given coordinates.
        Returns a DataProduct with local path to .hgt file (uncompressed).
        """
        if not HAS_REQUESTS:
            return DataProduct(
                name="srtm_dem",
                source="SRTM",
                format="hgt",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="requests library not installed"
            )
        
        start_time = time.time()
        if tile_name is None:
            tile_name = self._tile_name(lat, lon)
        
        # Check cache
        cached_path = os.path.join(self.cache_dir, f"{tile_name}.hgt")
        if os.path.exists(cached_path):
            print(f"Using cached SRTM tile: {cached_path}")
            return DataProduct(
                name=tile_name,
                source="SRTM",
                format="hgt",
                local_path=cached_path,
                metadata={"tile": tile_name, "lat": lat, "lon": lon, "cached": True},
                download_time_ms=(time.time() - start_time) * 1000,
                success=True
            )
        
        # Download compressed .hgt.gz
        url = f"{self.SRTM_BASE_URL}/{tile_name[0]}/{tile_name}.hgt.gz"
        gz_path = os.path.join(self.cache_dir, f"{tile_name}.hgt.gz")
        
        try:
            print(f"Downloading SRTM tile from {url}...")
            response = self.session.get(url, timeout=60)
            if response.status_code == 200:
                with open(gz_path, 'wb') as f:
                    f.write(response.content)
                
                # Decompress (using gzip)
                import gzip
                with gzip.open(gz_path, 'rb') as f_in:
                    with open(cached_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                
                # Remove compressed file
                os.remove(gz_path)
                
                download_time = (time.time() - start_time) * 1000
                print(f"SRTM tile downloaded and decompressed: {cached_path}")
                
                return DataProduct(
                    name=tile_name,
                    source="SRTM",
                    format="hgt",
                    local_path=cached_path,
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "size_bytes": os.path.getsize(cached_path)},
                    download_time_ms=download_time,
                    success=True
                )
            else:
                return DataProduct(
                    name=tile_name,
                    source="SRTM",
                    format="hgt",
                    local_path="",
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "status_code": response.status_code},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text[:200]}"
                )
        except Exception as e:
            return DataProduct(
                name=tile_name,
                source="SRTM",
                format="hgt",
                local_path="",
                metadata={"tile": tile_name, "lat": lat, "lon": lon},
                download_time_ms=(time.time() - start_time) * 1000,
                success=False,
                error=str(e)
            )
    
    def download_copernicus_tile(self, lat: float, lon: float, tile_name: Optional[str] = None) -> DataProduct:
        """
        Download Copernicus DEM 30m tile for given coordinates.
        Uses AWS Open Data (public, no authentication).
        Returns DataProduct with local path to .tif file.
        """
        if not HAS_REQUESTS:
            return DataProduct(
                name="copernicus_dem",
                source="Copernicus",
                format="tif",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="requests library not installed"
            )
        
        start_time = time.time()
        if tile_name is None:
            tile_name = self._tile_name(lat, lon)
        
        # Check cache
        cached_path = os.path.join(self.cache_dir, f"copernicus_{tile_name}.tif")
        if os.path.exists(cached_path):
            print(f"Using cached Copernicus tile: {cached_path}")
            return DataProduct(
                name=tile_name,
                source="Copernicus",
                format="tif",
                local_path=cached_path,
                metadata={"tile": tile_name, "lat": lat, "lon": lon, "cached": True},
                download_time_ms=(time.time() - start_time) * 1000,
                success=True
            )
        
        # Copernicus tile URL pattern (corrected based on AWS Open Data)
        copernicus_path = self._copernicus_tile_path(tile_name)
        url = f"{self.COPERNICUS_BASE_URL}/{copernicus_path}"
        
        try:
            print(f"Downloading Copernicus tile from {url}...")
            response = self.session.get(url, timeout=120)
            if response.status_code == 200:
                with open(cached_path, 'wb') as f:
                    f.write(response.content)
                
                download_time = (time.time() - start_time) * 1000
                print(f"Copernicus tile downloaded: {cached_path}")
                
                return DataProduct(
                    name=tile_name,
                    source="Copernicus",
                    format="tif",
                    local_path=cached_path,
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "size_bytes": os.path.getsize(cached_path)},
                    download_time_ms=download_time,
                    success=True
                )
            else:
                return DataProduct(
                    name=tile_name,
                    source="Copernicus",
                    format="tif",
                    local_path="",
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "status_code": response.status_code},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text[:200]}"
                )
        except Exception as e:
            return DataProduct(
                name=tile_name,
                source="Copernicus",
                format="tif",
                local_path="",
                metadata={"tile": tile_name, "lat": lat, "lon": lon},
                download_time_ms=(time.time() - start_time) * 1000,
                success=False,
                error=str(e)
            )
    
    def download_aster_gdem_tile(self, lat: float, lon: float, tile_name: Optional[str] = None) -> DataProduct:
        """
        Download ASTER Global DEM v3 tile (requires NASA Earthdata authentication).
        Uses CMR API to search for granules and downloads via Earthdata.
        """
        earthdata_session = self._get_earthdata_session()
        if earthdata_session is None:
            return DataProduct(
                name="aster_gdem",
                source="ASTER GDEM",
                format="tif",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="NASA Earthdata credentials required. Set EARTHDATA_USER and EARTHDATA_PASS environment variables."
            )
        
        start_time = time.time()
        if tile_name is None:
            tile_name = self._tile_name(lat, lon)
        
        # Check cache
        cached_path = os.path.join(self.cache_dir, f"aster_gdem_{tile_name}.tif")
        if os.path.exists(cached_path):
            print(f"Using cached ASTER GDEM tile: {cached_path}")
            return DataProduct(
                name=tile_name,
                source="ASTER GDEM",
                format="tif",
                local_path=cached_path,
                metadata={"tile": tile_name, "lat": lat, "lon": lon, "cached": True},
                download_time_ms=(time.time() - start_time) * 1000,
                success=True
            )
        
        # Compute bounding box for the tile (1 degree)
        # tile_name format: [NS]{2 digit lat}[EW]{3 digit lon}
        lat_prefix = tile_name[0]
        lat_deg = int(tile_name[1:3])
        lon_prefix = tile_name[3]
        lon_deg = int(tile_name[4:7])
        lat_min = -lat_deg if lat_prefix == 'S' else lat_deg
        lon_min = -lon_deg if lon_prefix == 'W' else lon_deg
        bbox = f"{lon_min},{lat_min},{lon_min+1},{lat_min+1}"
        
        # Search CMR for ASTER GDEM v3 granules
        search_params = {
            'short_name': 'ASTGTM',
            'version': '003',
            'bounding_box': bbox,
            'page_size': 1,
            'producer_provider_id': 'LPDAAC_ECS'
        }
        
        try:
            import tarfile
            import tempfile
            print(f"Searching CMR for ASTER GDEM tile covering {tile_name}...")
            search_response = earthdata_session.get(self.CMR_SEARCH_URL, params=search_params, timeout=30)
            if search_response.status_code != 200:
                return DataProduct(
                    name=tile_name,
                    source="ASTER GDEM",
                    format="tif",
                    local_path="",
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "status_code": search_response.status_code},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"CMR search failed: HTTP {search_response.status_code}"
                )
            
            search_data = search_response.json()
            granules = search_data.get('feed', {}).get('entry', [])
            if not granules:
                return DataProduct(
                    name=tile_name,
                    source="ASTER GDEM",
                    format="tif",
                    local_path="",
                    metadata={"tile": tile_name, "lat": lat, "lon": lon},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"No ASTER GDEM v3 granule found for tile {tile_name}"
                )
            
            # Get download URL from granule's links
            granule = granules[0]
            download_url = None
            for link in granule.get('links', []):
                if link.get('rel') == 'http://esipfed.org/ns/fedsearch/1.1/data#':
                    download_url = link.get('href')
                    break
            if download_url is None:
                # Try alternative link type
                for link in granule.get('links', []):
                    if 'data' in link.get('rel', ''):
                        download_url = link.get('href')
                        break
            
            if download_url is None:
                return DataProduct(
                    name=tile_name,
                    source="ASTER GDEM",
                    format="tif",
                    local_path="",
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "granule_id": granule.get('id')},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error="No download link found in granule"
                )
            
            print(f"Downloading ASTER GDEM tile from {download_url}...")
            download_response = earthdata_session.get(download_url, timeout=120, stream=True)
            if download_response.status_code != 200:
                return DataProduct(
                    name=tile_name,
                    source="ASTER GDEM",
                    format="tif",
                    local_path="",
                    metadata={"tile": tile_name, "lat": lat, "lon": lon, "status_code": download_response.status_code},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"Download failed: HTTP {download_response.status_code}"
                )
            
            # The download may be a .tar.gz file; we need to extract .tif
            # For simplicity, we'll assume the URL points directly to .tif (COG)
            # If it's a tar.gz, we need to extract. Let's check content-type.
            content_type = download_response.headers.get('Content-Type', '')
            if 'tar' in content_type or download_url.endswith('.tar.gz'):
                # Extract .tif from tar.gz
                import tarfile
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp:
                    for chunk in download_response.iter_content(chunk_size=8192):
                        tmp.write(chunk)
                    tmp_path = tmp.name
                
                with tarfile.open(tmp_path, 'r:gz') as tar:
                    # Find .tif member
                    tif_member = None
                    for member in tar.getmembers():
                        if member.name.endswith('.tif'):
                            tif_member = member
                            break
                    if tif_member is None:
                        os.remove(tmp_path)
                        return DataProduct(
                            name=tile_name,
                            source="ASTER GDEM",
                            format="tif",
                            local_path="",
                            metadata={"tile": tile_name, "lat": lat, "lon": lon},
                            download_time_ms=(time.time() - start_time) * 1000,
                            success=False,
                            error="No .tif file found in tar archive"
                        )
        except Exception as e:
            return DataProduct(
                name=tile_name,
                source="ASTER GDEM",
                format="tif",
                local_path="",
                metadata={"tile": tile_name, "lat": lat, "lon": lon},
                download_time_ms=(time.time() - start_time) * 1000,
                success=False,
                error=str(e)
            )
    
    def validate_dem_quality(self, dem_path: str) -> Dict[str, Any]:
        """
        Validate a DEM file for quality issues.
        Returns dict with quality metrics.
        """
        if not HAS_RASTERIO:
            return {'valid': False, 'error': 'rasterio not available'}
        
        try:
            with rasterio.open(dem_path) as src:
                data = src.read(1)
                total_pixels = data.size
                nodata = src.nodata if src.nodata is not None else -9999
                valid_mask = data != nodata
                valid_pixels = valid_mask.sum()
                coverage = valid_pixels / total_pixels if total_pixels > 0 else 0
                
                # Basic statistics
                stats = {
                    'min': float(data[valid_mask].min()) if valid_pixels > 0 else None,
                    'max': float(data[valid_mask].max()) if valid_pixels > 0 else None,
                    'mean': float(data[valid_mask].mean()) if valid_pixels > 0 else None,
                    'std': float(data[valid_mask].std()) if valid_pixels > 0 else None,
                }
                
                # Check for suspicious values (e.g., all zeros, extreme outliers)
                suspicious = False
                if stats['min'] is not None:
                    if stats['min'] == stats['max']:
                        suspicious = True  # constant values
                    if abs(stats['mean']) > 10000 or abs(stats['std']) > 5000:
                        suspicious = True  # unrealistic elevation range
                
                quality_score = coverage * (0.5 if not suspicious else 0.2)
                quality_score = min(max(quality_score, 0.0), 1.0)
                
                return {
                    'valid': True,
                    'coverage': coverage,
                    'suspicious': suspicious,
                    'stats': stats,
                    'quality_score': quality_score,
                    'nodata_value': nodata,
                    'shape': data.shape,
                    'crs': str(src.crs) if src.crs else None
                }
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def download_landsat_tile(self, lat: float, lon: float, date: str = None, band: str = "B4") -> DataProduct:
        """
        Download Landsat 8/9 OLI band tile (requires NASA Earthdata authentication).
        Placeholder for future implementation.
        """
        # TODO: Implement using USGS M2M API or CMR search
        return DataProduct(
            name=f"landsat_{band}",
            source="Landsat",
            format="tif",
            local_path="",
            metadata={"lat": lat, "lon": lon, "band": band},
            download_time_ms=0,
            success=False,
            error="Landsat download not yet implemented. Use Earthdata AppEEARS or USGS M2M API."
        )
    
    def download_gee_tile(self, lat: float, lon: float, collection: str = "COPERNICUS/DEM/GLO30", band: str = "DEM") -> DataProduct:
        """
        Download tile from Google Earth Engine (requires ee library and authentication).
        Placeholder for future implementation.
        """
        # TODO: Implement using earthengine-api
        return DataProduct(
            name=f"gee_{collection}_{band}",
            source="Google Earth Engine",
            format="tif",
            local_path="",
            metadata={"lat": lat, "lon": lon, "collection": collection, "band": band},
            download_time_ms=0,
            success=False,
            error="Google Earth Engine download not yet implemented. Install earthengine-api and authenticate."
        )
    
    def fetch_dem_tile(self, lat: float, lon: float, sources: List[str] = ["srtm", "copernicus"]) -> DataProduct:
        """
        Try multiple DEM sources in order until one succeeds.
        Args:
            lat, lon: Coordinates
            sources: List of sources to try, e.g., ["srtm", "copernicus", "aster"]
        Returns first successful DataProduct.
        """
        if not sources:
            return DataProduct(
                name="dem",
                source="multiple",
                format="",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="No DEM sources specified"
            )
        
        product = None
        for source in sources:
            if source == "srtm":
                product = self.download_srtm_tile(lat, lon)
            elif source == "copernicus":
                product = self.download_copernicus_tile(lat, lon)
            elif source == "aster":
                product = self.download_aster_gdem_tile(lat, lon)
            else:
                continue
            if product.success:
                return product
        # If all failed, return last product (with error)
        return product if product is not None else DataProduct(
            name="dem",
            source="multiple",
            format="",
            local_path="",
            metadata={},
            download_time_ms=0,
            success=False,
            error="No valid source found"
        )
    
    def fetch_ana_precipitation(self, station_code: str, start_date: str, end_date: str) -> DataProduct:
        """
        Fetch precipitation data from ANA HidroWeb API using new endpoint.
        Args:
            station_code: Code of the pluviometric station
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        Returns DataProduct with CSV file path.
        """
        if not HAS_REQUESTS:
            return DataProduct(
                name=f"ana_precip_{station_code}",
                source="ANA",
                format="csv",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="requests library not installed"
            )
        
        start_time = time.time()
        url = f"{self.ANA_HIDROWEB_BASE}/HidroSerieHistorica"
        # tipoDados=2 for precipitation, 3 for streamflow, 1 for level
        params = {
            'codEstacao': station_code,
            'dataInicio': start_date,
            'dataFim': end_date,
            'tipoDados': '2',  # precipitation
            'nivelConsistencia': ''  # both raw and processed
        }
        
        try:
            print(f"Fetching ANA precipitation data for station {station_code}...")
            response = self.session.get(url, params=params, timeout=60)
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                csv_path = os.path.join(self.cache_dir, f"ana_precip_{station_code}.csv")
                with open(csv_path, 'w') as f:
                    f.write("date,precipitation_mm\n")
                    records = 0
                    for serie in root.findall('.//SerieHistorica'):
                        # Each SerieHistorica contains daily values for a month
                        date_str = serie.findtext('DataHora')
                        if not date_str:
                            continue
                        # date_str format: YYYY-MM-DDTHH:MM:SS
                        year_month = date_str[:7]  # YYYY-MM
                        # Daily values are in Chuva01..Chuva31
                        for day in range(1, 32):
                            tag = f'Chuva{day:02d}'
                            value = serie.findtext(tag)
                            if value and value.strip():
                                try:
                                    precip = float(value)
                                    # Construct date
                                    from datetime import datetime
                                    try:
                                        date_obj = datetime.strptime(year_month, '%Y-%m')
                                        date_obj = date_obj.replace(day=day)
                                        date_formatted = date_obj.strftime('%Y-%m-%d')
                                        f.write(f"{date_formatted},{precip}\n")
                                        records += 1
                                    except ValueError:
                                        # Invalid date (e.g., February 31)
                                        pass
                                except ValueError:
                                    pass
                    # Close file
                download_time = (time.time() - start_time) * 1000
                print(f"ANA precipitation data saved: {csv_path}, records: {records}")
                
                return DataProduct(
                    name=f"ana_precip_{station_code}",
                    source="ANA",
                    format="csv",
                    local_path=csv_path,
                    metadata={
                        "station_code": station_code,
                        "start_date": start_date,
                        "end_date": end_date,
                        "records": records
                    },
                    download_time_ms=download_time,
                    success=True
                )
            else:
                return DataProduct(
                    name=f"ana_precip_{station_code}",
                    source="ANA",
                    format="csv",
                    local_path="",
                    metadata={"station_code": station_code, "status_code": response.status_code},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            return DataProduct(
                name=f"ana_precip_{station_code}",
                source="ANA",
                format="csv",
                local_path="",
                metadata={"station_code": station_code},
                download_time_ms=(time.time() - start_time) * 1000,
                success=False,
                error=str(e)
            )
    
    def generate_aster_swir(self, lat: float, lon: float, band: str = "SWIR1", size: int = 100) -> DataProduct:
        """
        Generate synthetic ASTER SWIR band data for given coordinates.
        In a real scenario, this would download from USGS EarthExplorer.
        For now, creates realistic synthetic data for testing mineral indices.
        Args:
            lat, lon: Center coordinates
            band: "SWIR1" (1.6 µm) or "SWIR2" (2.2 µm)
            size: Image size in pixels
        """
        if not HAS_NUMPY or not HAS_RASTERIO:
            return DataProduct(
                name=f"aster_{band}",
                source="ASTER (synthetic)",
                format="tif",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="numpy and rasterio required for synthetic generation"
            )
        
        start_time = time.time()
        
        # Create realistic synthetic SWIR data
        # Base reflectance typical of mineral surfaces
        if band == "SWIR1":
            base = 0.3
            variation = 0.15
        else:  # SWIR2
            base = 0.25
            variation = 0.12
        
        # Create spatial variation simulating mineral signatures
        x = np.linspace(0, 1, size)
        y = np.linspace(0, 1, size)
        xx, yy = np.meshgrid(x, y)
        
        # Mineral patterns (clay, iron oxide, etc.)
        clay_pattern = 0.1 * np.sin(20 * xx) * np.cos(20 * yy)
        iron_pattern = 0.05 * np.sin(40 * xx + 1) * np.cos(40 * yy + 2)
        noise = 0.02 * np.random.randn(size, size)
        
        reflectance = base + clay_pattern + iron_pattern + noise
        reflectance = np.clip(reflectance, 0, 1).astype(np.float32)
        
        # Save as GeoTIFF
        bounds = (lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05)
        transform = from_bounds(*bounds, size, size)
        
        output_path = os.path.join(self.cache_dir, f"aster_{band}_{lat:.2f}_{lon:.2f}.tif")
        
        profile = {
            'driver': 'GTiff',
            'height': size,
            'width': size,
            'count': 1,
            'dtype': 'float32',
            'crs': 'EPSG:4326',
            'transform': transform,
            'nodata': -9999
        }
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(reflectance, 1)
        
        download_time = (time.time() - start_time) * 1000
        print(f"Synthetic ASTER {band} generated: {output_path}")
        
        return DataProduct(
            name=f"aster_{band}",
            source="ASTER (synthetic)",
            format="tif",
            local_path=output_path,
            metadata={
                "lat": lat,
                "lon": lon,
                "band": band,
                "size": size,
                "note": "Synthetic data for testing mineral index workflows"
            },
            download_time_ms=download_time,
            success=True
        )
    
    def fetch_ana_stations(self, state: str = "CE", limit: int = 10) -> List[Dict]:
        """
        Fetch list of ANA hydrological stations for a given state using new HidroWeb API.
        """
        if not HAS_REQUESTS:
            return []
        
        url = f"{self.ANA_HIDROWEB_BASE}/HidroInventario"
        params = {
            'nmEstado': state,
            'tpEst': '2',  # 2 for pluviometric stations
            'telemetrica': ''  # all
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                stations = []
                count = 0
                for table in root.findall('.//Table'):
                    if count >= limit:
                        break
                    code = table.findtext('Codigo')
                    name = table.findtext('Nome')
                    lat = table.findtext('Latitude')
                    lon = table.findtext('Longitude')
                    altitude = table.findtext('Altitude')
                    state_name = table.findtext('nmEstado')
                    city = table.findtext('nmMunicipio')
                    river = table.findtext('RioNome')
                    station_type = table.findtext('TipoEstacao')
                    
                    stations.append({
                        'code': code,
                        'name': name,
                        'state': state_name,
                        'city': city,
                        'lat': float(lat) if lat else None,
                        'lon': float(lon) if lon else None,
                        'altitude': float(altitude) if altitude else None,
                        'river': river,
                        'type': station_type
                    })
                    count += 1
                return stations
        except Exception as e:
            print(f"Error fetching ANA stations: {e}")
        return []
    
    def search_ana_stations(self, 
                            name: Optional[str] = None, 
                            state: Optional[str] = None, 
                            basin: Optional[str] = None, 
                            lat: Optional[float] = None, 
                            lon: Optional[float] = None, 
                            radius_km: float = 10.0,
                            station_type: str = "plu",
                            limit: int = 50) -> List[Dict]:
        """
        Search ANA hydrological stations with various filters using new HidroWeb API.
        Args:
            name: Station name (partial match)
            state: State abbreviation (e.g., "SP", "RJ")
            basin: Basin name (not yet implemented)
            lat, lon: Center coordinates for radius search
            radius_km: Search radius in kilometers
            station_type: "plu" (pluviometric) or "flu" (fluviometric)
            limit: Maximum results
        """
        if not HAS_REQUESTS:
            return []
        
        url = f"{self.ANA_HIDROWEB_BASE}/HidroInventario"
        params = {
            'telemetrica': ''  # all
        }
        
        # Map station_type to tpEst: 1 for flu, 2 for plu
        if station_type == "flu":
            params['tpEst'] = '1'
        else:
            params['tpEst'] = '2'
        
        if name:
            params['nmEst'] = name
        if state:
            params['nmEstado'] = state
        # basin mapping requires basin code; skip for now
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                stations = []
                count = 0
                for table in root.findall('.//Table'):
                    if count >= limit:
                        break
                    station_lat = table.findtext('Latitude')
                    station_lon = table.findtext('Longitude')
                    # If radius filter provided, calculate distance
                    if lat is not None and lon is not None and station_lat and station_lon:
                        try:
                            station_lat_f = float(station_lat)
                            station_lon_f = float(station_lon)
                            dist_deg = math.sqrt((station_lat_f - lat)**2 + (station_lon_f - lon)**2)
                            dist_km = dist_deg * 111.0
                            if dist_km > radius_km:
                                continue
                        except ValueError:
                            pass
                    
                    stations.append({
                        'code': table.findtext('Codigo'),
                        'name': table.findtext('Nome'),
                        'state': table.findtext('nmEstado'),
                        'city': table.findtext('nmMunicipio'),
                        'basin': table.findtext('Bacia'),
                        'subbasin': table.findtext('SubBacia'),
                        'type': table.findtext('TipoEstacao'),
                        'lat': station_lat,
                        'lon': station_lon,
                        'altitude': table.findtext('Altitude'),
                        'status': None  # not in new API
                    })
                    count += 1
                return stations
        except Exception as e:
            print(f"Error searching ANA stations: {e}")
        return []
    
    def fetch_ana_streamflow(self, station_code: str, start_date: str, end_date: str) -> DataProduct:
        """
        Fetch streamflow data from ANA HidroWeb API (fluviometric stations).
        """
        if not HAS_REQUESTS:
            return DataProduct(
                name=f"ana_flow_{station_code}",
                source="ANA",
                format="csv",
                local_path="",
                metadata={},
                download_time_ms=0,
                success=False,
                error="requests library not installed"
            )
        
        start_time = time.time()
        url = f"{self.ANA_HIDROWEB_BASE}/serie/timeseries"
        params = {
            'codEst': station_code,
            'dataInicial': start_date.replace('-', ''),
            'dataFinal': end_date.replace('-', ''),
            'tipo': 'flu'  # fluviometric
        }
        
        try:
            print(f"Fetching ANA streamflow data for station {station_code}...")
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                csv_path = os.path.join(self.cache_dir, f"ana_flow_{station_code}.csv")
                with open(csv_path, 'w') as f:
                    f.write("date,flow_m3s\n")
                    for record in data.get('items', []):
                        date = record.get('dataHora')
                        flow = record.get('valor')
                        if date and flow:
                            day, month, year = date.split('/')
                            f.write(f"{year}-{month}-{day},{flow}\n")
                
                download_time = (time.time() - start_time) * 1000
                print(f"ANA streamflow data saved: {csv_path}")
                
                return DataProduct(
                    name=f"ana_flow_{station_code}",
                    source="ANA",
                    format="csv",
                    local_path=csv_path,
                    metadata={
                        "station_code": station_code,
                        "start_date": start_date,
                        "end_date": end_date,
                        "records": len(data.get('items', [])),
                        "type": "streamflow"
                    },
                    download_time_ms=download_time,
                    success=True
                )
            else:
                return DataProduct(
                    name=f"ana_flow_{station_code}",
                    source="ANA",
                    format="csv",
                    local_path="",
                    metadata={"station_code": station_code, "status_code": response.status_code},
                    download_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            return DataProduct(
                name=f"ana_flow_{station_code}",
                source="ANA",
                format="csv",
                local_path="",
                metadata={"station_code": station_code},
                download_time_ms=(time.time() - start_time) * 1000,
                success=False,
                error=str(e)
            )
    
    def get_supported_sources(self) -> Dict[str, str]:
        """Return dictionary of supported data sources"""
        return {
            'srtm': 'SRTM 30m DEM tiles (global)',
            'copernicus': 'Copernicus DEM 30m tiles (global)',
            'aster_gdem': 'ASTER Global DEM v3 (requires NASA Earthdata)',
            'ana_precipitation': 'ANA precipitation data (Brazil)',
            'ana_streamflow': 'ANA streamflow data (Brazil)',
            'aster_swir': 'ASTER SWIR bands (synthetic)'
        }


# Singleton instance
_fetcher = None

def get_fetcher(cache_dir: str = "./geospatial_cache") -> GeospatialDataFetcher:
    """Get or create singleton fetcher instance"""
    global _fetcher
    if _fetcher is None:
        _fetcher = GeospatialDataFetcher(cache_dir)
    return _fetcher


if __name__ == "__main__":
    # Quick test
    print("Testing GeospatialDataFetcher...")
    fetcher = get_fetcher()
    
    # Test SRTM download for a location in Brazil
    product = fetcher.download_srtm_tile(lat=-22.9, lon=-43.2)
    print(f"SRTM download: {product.success} - {product.local_path}")
    
    # Test ANA stations
    stations = fetcher.fetch_ana_stations(state="RJ", limit=5)
    print(f"Found {len(stations)} ANA stations")
    
    # Test synthetic ASTER
    product = fetcher.generate_aster_swir(lat=-22.9, lon=-43.2, band="SWIR1")
    print(f"ASTER synthetic: {product.success} - {product.local_path}")