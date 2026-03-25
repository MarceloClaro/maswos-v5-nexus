"""
Script para baixar e salvar dados geográficos do Crateús via geobr.
Executar primeiro para cachear os dados.
"""
from geobr import read_municipality, read_census_tract, read_weighting_area, read_neighborhood
import geopandas as gpd
import os

OUTPUT_DIR = "mcp-ecossistema-tese/output/geobr_data/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CRATEUS_CODE = 2304103

print("=" * 60)
print("BAIXANDO DADOS GEOBR PARA CRATEÚS")
print("=" * 60)

print("\n[1/4] Baixando limite municipal...")
muni = read_municipality(code_muni=CRATEUS_CODE, year=2020)
muni.to_file(f"{OUTPUT_DIR}crateus_municipio.geojson", driver="GeoJSON")
print(f"  OK: {len(muni)} registro(s)")
print(f"  Colunas: {list(muni.columns)}")

print("\n[2/4] Baixando setores censitários (2010)...")
tracts = read_census_tract(code_tract=CRATEUS_CODE, year=2010)
tracts.to_file(f"{OUTPUT_DIR}crateus_setores_censitarios.geojson", driver="GeoJSON")
print(f"  OK: {len(tracts)} setor(es) censitário(s)")
print(f"  Colunas: {list(tracts.columns)}")
print(f"  Zonas: {tracts['zone'].unique().tolist()}")

print("\n[3/4] Baixando áreas de ponderação...")
try:
    weighting = read_weighting_area(code_weighting=CRATEUS_CODE, year=2010)
    weighting.to_file(f"{OUTPUT_DIR}crateus_areas_ponderacao.geojson", driver="GeoJSON")
    print(f"  OK: {len(weighting)} área(s) de ponderação")
except Exception as e:
    print(f"  Aviso: {e}")
    weighting = None

print("\n[4/4] Baixando bairros (setores 2010)...")
try:
    neighborhoods = read_neighborhood(year=2010)
    crateus_neighborhoods = neighborhoods[neighborhoods['code_muni'] == CRATEUS_CODE]
    if len(crateus_neighborhoods) > 0:
        crateus_neighborhoods.to_file(f"{OUTPUT_DIR}crateus_bairros.geojson", driver="GeoJSON")
        print(f"  OK: {len(crateus_neighborhoods)} bairro(s)")
    else:
        print("  Nenhum bairro encontrado para Crateús")
except Exception as e:
    print(f"  Aviso: {e}")

print("\n" + "=" * 60)
print("DADOS SALVOS EM:", OUTPUT_DIR)
print("=" * 60)
print("\nArquivos gerados:")
for f in os.listdir(OUTPUT_DIR):
    size = os.path.getsize(f"{OUTPUT_DIR}{f}") / 1024
    print(f"  - {f} ({size:.1f} KB)")

print("\n" + "=" * 60)
print("RESUMO DOS DADOS")
print("=" * 60)
print(f"\nMunicípio de Crateús:")
print(f"  Código IBGE: {CRATEUS_CODE}")
print(f"  Setores censitários: {len(tracts)}")
print(f"  Área urbana: {len(tracts[tracts['zone'] == 'urban'])} setores")
print(f"  Área rural: {len(tracts[tracts['zone'] == 'rural'])} setores")

print("\nEstatísticas dos setores censitários:")
print(tracts[['code_tract', 'zone', 'name_muni']].groupby('zone').count())
