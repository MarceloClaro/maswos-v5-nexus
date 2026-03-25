"""
Mapas Profissionais para Tese de Doutorado - MCP e Educacao noertao do Ceara
Versao Limpa e Profissional
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'output/mapas/'

def get_brazil_states():
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    return gpd.read_file(url)

def create_brazil_map():
    """Mapa do Brasil profissional"""
    print("Gerando mapa do Brasil...")
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    outras = states[~states['sigla'].isin(nordeste)]
    gpd.GeoSeries(outras.geometry.values).plot(ax=ax, color='#E0E0E0', 
                                                edgecolor='#999999', linewidth=0.5)
    
    ne_states = states[states['sigla'].isin(nordeste)]
    gpd.GeoSeries(ne_states.geometry.values).plot(ax=ax, color='#FF6B35', 
                                                   edgecolor='#CC4400', linewidth=1.5)
    
    for idx, row in ne_states.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                   fontsize=10, ha='center', va='center', fontweight='bold', color='white')
    
    ax.set_title('Mapa do Brasil: Regiao Nordeste', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_xlim(-75, -30)
    ax.set_ylim(-35, 6)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    ax.legend(handles=[
        mpatches.Patch(color='#FF6B35', label='Nordeste'),
        mpatches.Patch(color='#E0E0E0', label='Outras Regioes')
    ], loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_brasil_nordeste.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK]")

def create_northeast_map():
    """Mapa do Nordeste profissional"""
    print("Gerando mapa do Nordeste...")
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    cores = ['#FF6B35', '#FFD700', '#32CD32', '#1E90FF', '#FF1493',
            '#8A2BE2', '#00CED1', '#FF6347', '#4682B4']
    
    ne_states = states[states['sigla'].isin(nordeste)]
    for i, (idx, row) in enumerate(ne_states.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(ax=ax, color=cores[i], edgecolor='black', linewidth=1)
        centroid = row.geometry.centroid
        ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                   fontsize=14, ha='center', va='center', fontweight='bold', color='white')
    
    ax.set_title('Regiao Nordeste do Brasil', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_xlim(-48, -32)
    ax.set_ylim(-16, -1)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_nordeste.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK]")

def create_ceara_map():
    """Mapa do Ceara profissional"""
    print("Gerando mapa do Ceara...")
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    ceara = states[states['sigla'] == 'CE']
    gpd.GeoSeries(ceara.geometry.values).plot(ax=ax, facecolor='#FFB347', edgecolor='black', linewidth=2)
    
    vizinhos = states[states['sigla'].isin(['PI', 'RN', 'PB'])]
    gpd.GeoSeries(vizinhos.geometry.values).plot(ax=ax, facecolor='#E8E8E8', edgecolor='#999', linewidth=0.8)
    
    centroid = ceara.geometry.iloc[0].centroid
    ax.annotate('CEARA', xy=(centroid.x, centroid.y), fontsize=24, ha='center', va='center',
               fontweight='bold', color='white')
    
    # Marker simples para Crateus
    ax.plot(-40.4108, -5.7433, 'o', markersize=8, color='red', markeredgecolor='darkred', zorder=10)
    ax.annotate('Crateus', xy=(-40.4108, -5.7433), xytext=(5, 5), textcoords='offset points',
               fontsize=10, fontweight='bold')
    
    ax.set_title('Estado do Ceara', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_xlim(-42, -36.5)
    ax.set_ylim(-8.5, -2.5)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_ceara_crateus.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK]")

def create_crateus_detail_map():
    """Mapa de Crateus profissional"""
    print("Gerando mapa de Crateus...")
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    
    # Zonas de influencia simples
    circle1 = plt.Circle((crateus_lon, crateus_lat), 0.5, fill=True, color='#FF6B6B', alpha=0.15)
    ax.add_patch(circle1)
    
    # Marker simples para IFCE
    ax.plot(crateus_lon, crateus_lat, 'o', markersize=10, color='red', markeredgecolor='darkred', zorder=10)
    ax.annotate('IFCE Crateus', xy=(crateus_lon, crateus_lat), xytext=(0.5, 0.5),
               fontsize=11, fontweight='bold', arrowprops=dict(arrowstyle='->', color='red'))
    
    # Cidades proximas
    cidades = {
        'Tamboril': (-4.79, -40.82), 'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74), 'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47), 'Santa Quiteria': (-4.33, -40.15)
    }
    for cidade, (lat, lon) in cidades.items():
        ax.plot(lon, lat, 'o', markersize=6, color='#228B22', zorder=5)
        ax.annotate(cidade, xy=(lon, lat), xytext=(0.2, 0.2), fontsize=9,
                   arrowprops=dict(arrowstyle='->', color='green'))
    
    ax.set_title('Regiao de Crateus - Sertao do Ceara', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_xlim(-41.5, -38)
    ax.set_ylim(-7, -4)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_detalhe.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK]")
    
    # HTML
    import folium
    m = folium.Map(location=[crateus_lat, crateus_lon], zoom_start=8)
    folium.Marker([crateus_lat, crateus_lon], popup='IFCE Campus Crateus').add_to(m)
    m.save(f'{OUTPUT_DIR}mapa_crateus_detalhe.html')

def create_interactive_map():
    """Mapa interativo"""
    print("Gerando mapa interativo...")
    import folium
    
    m = folium.Map(location=[-10.0, -40.0], zoom_start=5)
    
    estados = {
        'Maranhao': (-2.5, -44.3), 'Piaui': (-5.1, -42.8), 'Ceara': (-5.2, -39.0),
        'RN': (-5.4, -36.5), 'Paraiba': (-7.1, -35.0), 'Pernambuco': (-8.4, -37.9),
        'Alagoas': (-9.6, -36.0), 'Sergipe': (-10.9, -37.5), 'Bahia': (-12.6, -41.9)
    }
    
    for nome, coords in estados.items():
        folium.CircleMarker([coords[0], coords[1]], radius=15, color='#FF6B35',
                           fill=True, fillColor='#FF6B35', fillOpacity=0.7,
                           popup=f'<b>{nome}</b>').add_to(m)
    
    folium.Marker([-5.7433, -40.4108], popup='IFCE Crateus').add_to(m)
    
    m.save(f'{OUTPUT_DIR}mapa_interativo_completo.html')
    print("[OK]")

def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 50)
    print("  MAPAS PROFISSIONAIS - TESE MCP")
    print("=" * 50)
    
    create_brazil_map()
    create_northeast_map()
    create_ceara_map()
    create_crateus_detail_map()
    create_interactive_map()
    
    print("=" * 50)
    print("  TODOS OS MAPAS GERADOS!")
    print("=" * 50)

if __name__ == '__main__':
    main()
