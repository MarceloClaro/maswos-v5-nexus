"""
Script de Geracao de Mapas com Contornos Reais - Brasil, Nordeste, Ceara, Crateus
Tese de Doutorado - MCP e Educacao noertao do Ceara
Versao com plot direto do geodataframe
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'output/mapas/'

def get_brazil_states():
    """Baixa dados reais dos estados brasileiros"""
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    return gpd.read_file(url)

def create_brazil_map():
    """Mapa do Brasil com contornos reais"""
    print("Gerando mapa do Brasil com contornos...")
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    # Plot其他states primeiro
    outras = states[~states['sigla'].isin(nordeste)]
    outras.plot(ax=ax, color='#D3D3D3', edgecolor='#808080', linewidth=0.8)
    
    # Plot Nordeste
    ne_states = states[states['sigla'].isin(nordeste)]
    ne_states.plot(ax=ax, color='#FF6B35', edgecolor='#CC5500', linewidth=2)
    
    # Add labels for Nordeste
    for idx, row in ne_states.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                   fontsize=12, ha='center', va='center',
                   fontweight='bold', color='white',
                   path_effects=[path_effects.withStroke(linewidth=4, foreground='black')])
    
    ax.set_xlim(-75, -30)
    ax.set_ylim(-35, 6)
    ax.set_title('Mapa do Brasil: Destaque para a Regiao Nordeste\n(Tese: MCP e Educacao noertao do Ceara)',
                fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.set_facecolor('#E8F4F8')
    
    ax.legend(handles=[
        mpatches.Patch(color='#FF6B35', label='Nordeste (9 Estados)'),
        mpatches.Patch(color='#D3D3D3', label='Outras Regioes')
    ], loc='lower right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_brasil_nordeste.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Brasil salvo")

def create_northeast_map():
    """Mapa detalhado do Nordeste com contornos reais"""
    print("Gerando mapa do Nordeste com contornos...")
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    nordeste_codes = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    nordeste_names = {
        'MA': 'Maranhao', 'PI': 'Piau', 'CE': 'Ceara',
        'RN': 'R.G.Norte', 'PB': 'Paraiba', 'PE': 'Pernambuco',
        'AL': 'Alagoas', 'SE': 'Sergipe', 'BA': 'Bahia'
    }
    
    cores = ['#FF6B35', '#FFD700', '#32CD32', '#1E90FF', '#FF1493',
            '#8A2BE2', '#00CED1', '#FF6347', '#4682B4']
    
    ne_states = states[states['sigla'].isin(nordeste_codes)].copy()
    
    for i, (idx, row) in enumerate(ne_states.iterrows()):
        color = cores[i]
        gpd.GeoSeries([row.geometry]).plot(ax=ax, color=color, 
                                           edgecolor='black', linewidth=2.5)
        
        centroid = row.geometry.centroid
        ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                   fontsize=16, ha='center', va='center',
                   fontweight='bold', color='white',
                   path_effects=[path_effects.withStroke(linewidth=4, foreground='black')])
        
        ax.annotate(nordeste_names.get(row['sigla'], ''),
                   xy=(centroid.x, centroid.y - 1.5),
                   fontsize=10, ha='center', style='italic', color='#222')
    
    ax.set_xlim(-48, -32)
    ax.set_ylim(-16, -1)
    ax.set_title('Mapa da Regiao Nordeste do Brasil\n(Estados Incluidos no Estudo)',
                fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_facecolor('#E8F4FF')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_nordeste.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Nordeste salvo")

def create_ceara_map():
    """Mapa do Ceara com contorno real"""
    print("Gerando mapa do Ceara com contorno...")
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    ceara = states[states['sigla'] == 'CE']
    gpd.GeoSeries(ceara.geometry.values).plot(ax=ax, facecolor='#FFB347', 
                                                   edgecolor='black', linewidth=4)
    
    ceara_geom = ceara.geometry.iloc[0]
    centroid = ceara_geom.centroid
    ax.annotate('CEARA', xy=(centroid.x, centroid.y),
               fontsize=28, ha='center', va='center',
               fontweight='bold', color='white',
               path_effects=[path_effects.withStroke(linewidth=5, foreground='#CC7700')])
    
    # Plotar estados vizinhos
    vizinhos = states[states['sigla'].isin(['PI', 'RN', 'PB'])]
    gpd.GeoSeries(vizinhos.geometry.values).plot(ax=ax, facecolor='#E0E0E0',
                                                   edgecolor='gray', linewidth=1)
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    ax.plot(crateus_lon, crateus_lat, '*', markersize=600, color='red',
           markeredgecolor='darkred', markeredgewidth=4, zorder=10)
    
    ax.annotate('CRATEUS\n(IFCE Campus)',
               xy=(crateus_lon, crateus_lat),
               xytext=(crateus_lon + 1.8, crateus_lat + 1.5),
               fontsize=14, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color='red', lw=3),
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                       edgecolor='red', linewidth=2))
    
    outras = {
        'Fortaleza': (-3.71, -38.54),
        'Sobral': (-3.69, -40.37),
        'Quixada': (-4.97, -39.01),
        'Juazeiro': (-7.21, -39.30)
    }
    for cidade, (lat, lon) in outras.items():
        ax.plot(lon, lat, 'o', markersize=150, color='#555',
               alpha=0.8, markeredgecolor='black', zorder=5)
        ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.4, lat+0.4),
                   fontsize=11, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax.set_xlim(-42, -36.5)
    ax.set_ylim(-8.5, -2)
    ax.set_title('Mapa do Estado do Ceara\nDestaque para a Cidade de Crateus',
                fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_facecolor('#FFF8DC')
    
    legend = [
        mpatches.Patch(color='#FFB347', label='Ceara'),
        mpatches.Patch(color='#E0E0E0', label='Estados Vizinhos'),
        plt.Line2D([0], [0], marker='*', color='w', label='IFCE Campus Crateus',
                  markerfacecolor='red', markersize=20, markeredgecolor='darkred'),
    ]
    ax.legend(handles=legend, loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_ceara_crateus.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Ceara salvo")

def create_crateus_detail_map():
    """Mapa detalhado de Crateus"""
    print("Gerando mapa detalhado de Crateus...")
    fig, ax = plt.subplots(1, 1, figsize=(14, 14))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    
    # Fundo
    ax.set_facecolor('#F5FFFA')
    
    # IFCE Campus
    ax.plot(crateus_lon, crateus_lat, '*', markersize=600, color='red',
           markeredgecolor='darkred', markeredgewidth=4, zorder=10)
    
    ax.annotate('IFCE Campus Crateus',
               xy=(crateus_lon, crateus_lat),
               xytext=(crateus_lon - 1.8, crateus_lat + 1.2),
               fontsize=16, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFF00',
                       edgecolor='red', linewidth=2))
    
    # circulo de influencia
    circle = plt.Circle((crateus_lon, crateus_lat), 0.8, fill=False,
                       color='blue', linestyle='--', linewidth=3)
    ax.add_patch(circle)
    ax.annotate('Zona de Influencia (50km)',
               xy=(crateus_lon + 1.0, crateus_lat - 0.5),
               fontsize=12, color='blue', fontweight='bold')
    
    # Cidades do entorno
    cidades = {
        'Tamboril': (-4.79, -40.82),
        'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74),
        'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47),
        'Santa Quiteria': (-4.33, -40.15)
    }
    
    for cidade, (lat, lon) in cidades.items():
        ax.plot(lon, lat, 's', markersize=120, color='#228B22',
               alpha=0.85, markeredgecolor='black', zorder=5)
        ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.25, lat+0.25),
                   fontsize=11, arrowprops=dict(arrowstyle='->', color='#228B22'))
    
    ax.set_xlim(-42.5, -37.5)
    ax.set_ylim(-8, -3.5)
    ax.set_title('Mapa de Crateus e Regiao do Sertao do Ceara\n(Area de Estudo)',
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.4)
    
    legend = [
        plt.Line2D([0], [0], marker='*', color='w', label='IFCE Campus Crateus',
                  markerfacecolor='red', markersize=24, markeredgecolor='darkred'),
        plt.Line2D([0], [0], marker='s', color='w', label='Municipios do Entorno',
                  markerfacecolor='#228B22', markersize=14),
        mpatches.Patch(color='blue', label='Zona de Influencia', fill=False, linewidth=2)
    ]
    ax.legend(handles=legend, loc='upper right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_detalhe.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa detalhado de Crateus salvo")
    
    # HTML interativo
    import folium
    m = folium.Map(location=[crateus_lat, crateus_lon], zoom_start=9)
    folium.Marker([crateus_lat, crateus_lon],
                  popup='<b>IFCE Campus Crateus</b>',
                  icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')).add_to(m)
    folium.Circle([crateus_lat, crateus_lon], radius=20000, color='blue',
                  fill=True, fillOpacity=0.2).add_to(m)
    m.save(f'{OUTPUT_DIR}mapa_crateus_detalhe.html')
    print("[OK] Mapa HTML salvo")

def create_interactive_map():
    """Mapa interativo completo"""
    print("Gerando mapa interativo...")
    import folium
    
    m = folium.Map(location=[-10.0, -40.0], zoom_start=5, tiles='CartoDB positron')
    folium.TileLayer('OpenStreetMap', attr='OpenStreetMap').add_to(m)
    
    fg_n = folium.FeatureGroup(name='Nordeste')
    fg_c = folium.FeatureGroup(name='Crateus')
    
    estados = {
        'Maranhao': (-2.5, -44.3), 'Piaui': (-5.1, -42.8), 'Ceara': (-5.2, -39.0),
        'RN': (-5.4, -36.5), 'Paraiba': (-7.1, -35.0), 'Pernambuco': (-8.4, -37.9),
        'Alagoas': (-9.6, -36.0), 'Sergipe': (-10.9, -37.5), 'Bahia': (-12.6, -41.9)
    }
    
    for nome, coords in estados.items():
        folium.CircleMarker([coords[0], coords[1]], radius=22, color='#FF6B35',
                           fill=True, fillColor='#FF6B35', fillOpacity=0.7,
                           popup=f'<b>{nome}</b>').add_to(fg_n)
    
    folium.Marker([-5.7433, -40.4108],
                  popup='<b>IFCE Campus Crateus</b>',
                  icon=folium.Icon(color='red', icon='university', prefix='fa')).add_to(fg_c)
    
    fg_n.add_to(m)
    fg_c.add_to(m)
    folium.LayerControl().add_to(m)
    m.save(f'{OUTPUT_DIR}mapa_interativo_completo.html')
    print("[OK] Mapa interativo salvo")

def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 55)
    print("  GERACAO DE MAPAS COM CONTORNOS REAIS - TESE MCP")
    print("=" * 55)
    
    create_brazil_map()
    create_northeast_map()
    create_ceara_map()
    create_crateus_detail_map()
    create_interactive_map()
    
    print("=" * 55)
    print("  TODOS OS MAPAS GERADOS COM SUCESSO!")
    print("=" * 55)
    print(f"\nArquivos em: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
