"""
Script de Geracao de TODOS os Mapas - Versao Completa e Melhorada
Tese de Doutorado - MCP e Educacao noertao do Ceara
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.patches import Circle
try:
    import contextily as ctx
except:
    ctx = None
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'output/mapas/'

def get_brazil_states():
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    return gpd.read_file(url)

def create_brazil_map():
    """Mapa do Brasil completo melhorado"""
    print("Gerando mapa do Brasil...")
    fig, ax = plt.subplots(1, 1, figsize=(22, 18))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    # Fundo
    ax.set_facecolor('#E8F4F8')
    ax.set_xlim(-75, -30)
    ax.set_ylim(-35, 6)
    
    # Mapa de satelite (ignora erros se nao disponivel)
    try:
        ctx.add_basemap(ax, crs='EPSG:4326')
    except:
        pass
    
    # Legenda
    legend = [
        mpatches.Patch(color='#FF6B35', label='Nordeste (9 Estados)'),
        mpatches.Patch(color='#D3D3D3', label='Outras Regioes'),
    ]
    ax.legend(handles=legend, loc='lower right', fontsize=10, 
             framealpha=0.95, title='LEGENDA', title_fontsize=11, markerscale=0.8)
    
    # Barra de escala
    ax.plot([-70, -65], [-32, -32], 'k-', linewidth=4)
    ax.plot([-70, -70], [-32.3, -31.7], 'k-', linewidth=4)
    ax.plot([-65, -65], [-32.3, -31.7], 'k-', linewidth=4)
    ax.text(-67.5, -33.5, '~500 km', ha='center', fontsize=11)
    
    # Rosa do vento
    ax.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
               fontsize=18, fontweight='bold', ha='center')
    ax.annotate('^', xy=(0.97, 0.93), xycoords='axes fraction',
               fontsize=24, ha='center', color='gray')
    
    # Info box
    info = """BRASIL
- Area total: 8.510.000 km²
- Regiao Nordeste: 9 Estados
- Populacao NE: ~57 milhoes"""
    ax.text(0.02, 0.02, info, transform=ax.transAxes,
           fontsize=10, va='bottom', ha='left',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_brasil_nordeste.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Brasil salvo")

def create_northeast_map():
    """Mapa do Nordeste completo"""
    print("Gerando mapa do Nordeste...")
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    nomes = {
        'MA': 'Maranhao', 'PI': 'Piaui', 'CE': 'Ceara',
        'RN': 'Rio G. Norte', 'PB': 'Paraiba', 'PE': 'Pernambuco',
        'AL': 'Alagoas', 'SE': 'Sergipe', 'BA': 'Bahia'
    }
    capitais = {
        'Sao Luis': (-2.53, -44.30), 'Teresina': (-5.08, -42.80),
        'Fortaleza': (-3.71, -38.54), 'Natal': (-5.79, -35.20),
        'Joao Pessoa': (-7.11, -34.86), 'Recife': (-8.04, -34.92),
        'Maceio': (-9.66, -35.73), 'Aracaju': (-10.90, -37.07),
        'Salvador': (-12.97, -38.50)
    }
    
    cores = ['#FF6B35', '#FFD700', '#32CD32', '#1E90FF', '#FF1493',
            '#8A2BE2', '#00CED1', '#FF6347', '#4682B4']
    
    ax.set_facecolor('#E8F4FF')
    
    ne_states = states[states['sigla'].isin(nordeste)]
    
    for i, (idx, row) in enumerate(ne_states.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(ax=ax, color=cores[i], 
                                           edgecolor='black', linewidth=2.5)
        
        centroid = row.geometry.centroid
        ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                   fontsize=18, ha='center', va='center',
                   fontweight='bold', color='white',
                   path_effects=[path_effects.withStroke(linewidth=4, foreground='black')])
        
        ax.annotate(nomes.get(row['sigla'], ''),
                   xy=(centroid.x, centroid.y - 1.3),
                   fontsize=11, ha='center', style='italic', color='#222')
    
    # Plotar capitais
    for capital, (lat, lon) in capitais.items():
        ax.plot(lon, lat, 'D', markersize=50, color='#FFD700',
               markeredgecolor='black', markeredgewidth=1.5, zorder=8)
        ax.annotate(capital, xy=(lon, lat), xytext=(lon+0.3, lat+0.3),
                   fontsize=9, fontweight='bold', color='#333',
                   arrowprops=dict(arrowstyle='->', color='gray'))
    
    # Titulo
    ax.set_title('MAPA DA REGIÃO NORDESTE DO BRASIL\n(9 Estados e Capitais)',
                fontsize=22, fontweight='bold', pad=25)
    
    ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
    ax.set_xlim(-48, -32)
    ax.set_ylim(-16, -1)
    ax.grid(True, linestyle='--', alpha=0.4)
    
    # Legenda
    legend = [
        mpatches.Patch(color='#FFD700', label='Capitais'),
    ]
    ax.legend(handles=legend, loc='lower right', fontsize=10, markerscale=0.8)
    
    # Barra de escala
    ax.plot([-46, -43], [-15, -15], 'k-', linewidth=4)
    ax.plot([-46, -46], [-15.3, -14.7], 'k-', linewidth=4)
    ax.plot([-43, -43], [-15.3, -14.7], 'k-', linewidth=4)
    ax.text(-44.5, -15.8, '~300 km', ha='center', fontsize=11)
    
    # Info
    info = """NORDESTE
- 9 Estados
- Area: ~1.540.000 km²
- Populacao: ~57 milhoes
- IDH Medio: 0.731"""
    ax.text(0.02, 0.02, info, transform=ax.transAxes,
           fontsize=10, va='bottom', ha='left',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_nordeste.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Nordeste salvo")

def create_ceara_map():
    """Mapa do Ceara completo"""
    print("Gerando mapa do Ceara...")
    fig, ax = plt.subplots(1, 1, figsize=(18, 16))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    ceara = states[states['sigla'] == 'CE']
    gpd.GeoSeries(ceara.geometry.values).plot(ax=ax, facecolor='#FFB347', 
                                                   edgecolor='black', linewidth=4)
    
    # Estados vizinhos
    vizinhos = states[states['sigla'].isin(['PI', 'RN', 'PB'])]
    gpd.GeoSeries(vizinhos.geometry.values).plot(ax=ax, facecolor='#E0E0E0',
                                                   edgecolor='gray', linewidth=1)
    
    ceara_geom = ceara.geometry.iloc[0]
    centroid = ceara_geom.centroid
    ax.annotate('CEARA', xy=(centroid.x, centroid.y),
               fontsize=32, ha='center', va='center',
               fontweight='bold', color='white',
               path_effects=[path_effects.withStroke(linewidth=5, foreground='#CC7700')])
    
    # Principais cidades
    cidades = {
        'Fortaleza': (-3.71, -38.54, 'capital'),
        'Crateus': (-5.7433, -40.4108, 'ifce'),
        'Sobral': (-3.69, -40.37, 'principal'),
        'Juazeiro': (-7.21, -39.30, 'principal'),
        'Quixada': (-4.97, -39.01, 'municipio'),
        'Iguatu': (-6.24, -39.30, 'municipio'),
        'Cascavel': (-3.97, -38.24, 'municipio'),
        'Caninde': (-4.35, -39.46, 'municipio'),
    }
    
    for cidade, (lat, lon, tipo) in cidades.items():
        if tipo == 'ifce':
            ax.plot(lon, lat, '*', markersize=100, color='red',
                   markeredgecolor='darkred', markeredgewidth=1.5, zorder=10)
            ax.annotate(f'{cidade}\n(IFCE)', xy=(lon, lat),
                       xytext=(lon + 1.5, lat + 0.8),
                       fontsize=10, fontweight='bold', color='red',
                       arrowprops=dict(arrowstyle='->', color='red', lw=2),
                       bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
        elif tipo == 'capital':
            ax.plot(lon, lat, 'D', markersize=60, color='#FFD700',
                   markeredgecolor='black', markeredgewidth=1.5, zorder=8)
            ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.4, lat+0.4),
                       fontsize=9, fontweight='bold', arrowprops=dict(arrowstyle='->', color='gray'))
        else:
            ax.plot(lon, lat, 'o', markersize=50, color='#333',
                   alpha=0.8, markeredgecolor='black', zorder=5)
            ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.3, lat+0.3),
                       fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax.set_xlim(-42, -36.5)
    ax.set_ylim(-8.5, -2.5)
    ax.set_title('MAPA DO ESTADO DO CEARA\nDestaque para Crateus e Principais Cidades',
                fontsize=22, fontweight='bold', pad=25)
    ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_facecolor('#FFF8DC')
    
    # Legenda
    legend = [
        mpatches.Patch(color='#FFB347', label='Ceara'),
        mpatches.Patch(color='#E0E0E0', label='Estados Vizinhos'),
        plt.Line2D([0], [0], marker='*', color='w', label='IFCE Crateus',
                  markerfacecolor='red', markersize=8, markeredgecolor='darkred'),
        plt.Line2D([0], [0], marker='D', color='w', label='Capital (Fortaleza)',
                  markerfacecolor='#FFD700', markersize=6),
    ]
    ax.legend(handles=legend, loc='lower right', fontsize=10, markerscale=0.8)
    
    # Barra de escala
    ax.plot([-41, -38.5], [-7.8, -7.8], 'k-', linewidth=4)
    ax.plot([-41, -41], [-8.1, -7.5], 'k-', linewidth=4)
    ax.plot([-38.5, -38.5], [-8.1, -7.5], 'k-', linewidth=4)
    ax.text(-39.75, -8.5, '~250 km', ha='center', fontsize=11)
    
    # Info
    info = """CEARA
- Area: 148.825 km²
- Populacao: ~9.2 milhoes
- Capital: Fortaleza
- Regiao: Nordeste"""
    ax.text(0.02, 0.02, info, transform=ax.transAxes,
           fontsize=10, va='bottom', ha='left',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_ceara_crateus.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Ceara salvo")

def create_crateus_detail_map():
    """Mapa detalhado de Crateus"""
    print("Gerando mapa de Crateus...")
    fig, ax = plt.subplots(1, 1, figsize=(18, 18))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    ax.set_facecolor('#F0FFF0')
    
    # Zonas de influencia
    circle1 = Circle((crateus_lon, crateus_lat), 0.35, fill=True,
                    color='#FF6B6B', alpha=0.2)
    ax.add_patch(circle1)
    
    circle2 = Circle((crateus_lon, crateus_lat), 0.60, fill=True,
                    color='#4ECDC4', alpha=0.15)
    ax.add_patch(circle2)
    
    circle3 = Circle((crateus_lon, crateus_lat), 0.95, fill=True,
                    color='#45B7D1', alpha=0.1)
    ax.add_patch(circle3)
    
    # IFCE com brilho (reduzido)
    for i in range(3):
        size = 80 + i * 40
        ax.plot(crateus_lon, crateus_lat, '*', markersize=size, color='yellow',
               alpha=0.3 - i*0.1, zorder=5)
    
    ax.plot(crateus_lon, crateus_lat, '*', markersize=120, color='#FF0000',
           markeredgecolor='#8B0000', markeredgewidth=2, zorder=15)
    
    ax.annotate('IFCE - CAMPUS CRATEUS\n(POLO PRINCIPAL)',
               xy=(crateus_lon, crateus_lat),
               xytext=(crateus_lon - 2.8, crateus_lat + 1.8),
               fontsize=15, fontweight='bold', color='#8B0000',
               arrowprops=dict(arrowstyle='->', color='#8B0000', lw=2.5),
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFFACD',
                       edgecolor='#8B0000', linewidth=3))
    
    # Municipios
    cidades = {
        'Crateus': (-5.7433, -40.4108),
        'Tamboril': (-4.79, -40.82),
        'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74),
        'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47),
        'Santa Quiteria': (-4.33, -40.15),
        'Senador Pompeu': (-5.58, -39.37),
        'Quixada': (-4.97, -39.01),
        'Sobral': (-3.69, -40.37),
        'Fortaleza': (-3.71, -38.54),
    }
    
    for cidade, (lat, lon) in cidades.items():
        if cidade == 'Crateus':
            continue
        
        ax.plot(lon, lat, 's', markersize=60, color='#228B22',
               alpha=0.9, markeredgecolor='black', markeredgewidth=1.5, zorder=8)
        ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.25, lat+0.25),
                   fontsize=10, fontweight='bold', color='#006400',
                   arrowprops=dict(arrowstyle='->', color='#228B22', lw=1.5))
    
    # Estradas
    ax.plot([-40.41, -38.54], [-5.74, -3.71], '--', color='#666', linewidth=1.5, alpha=0.5)
    ax.plot([-40.41, -40.37], [-5.74, -3.69], '--', color='#666', linewidth=1.5, alpha=0.5)
    
    ax.set_xlim(-42.5, -37)
    ax.set_ylim(-8, -3)
    ax.set_title('MAPA DA REGIÃO DE CRATEUS - SERTÃO DO CEARÁ\n(Área de Estudo: IFCE e Municípios do Entorno)',
                fontsize=20, fontweight='bold', pad=25)
    ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.4)
    
    # Legenda
    legend = [
        plt.Line2D([0], [0], marker='*', color='w', label='IFCE Campus Crateus',
                  markerfacecolor='#FF0000', markersize=10, markeredgecolor='#8B0000'),
        plt.Line2D([0], [0], marker='s', color='w', label='Municipios',
                  markerfacecolor='#228B22', markersize=8),
        mpatches.Patch(color='#FF6B6B', alpha=0.3, label='Zona 30km'),
        mpatches.Patch(color='#4ECDC4', alpha=0.2, label='Zona 50km'),
        mpatches.Patch(color='#45B7D1', alpha=0.15, label='Zona 80km'),
    ]
    ax.legend(handles=legend, loc='upper left', fontsize=8, framealpha=0.95, markerscale=0.6)
    
    # Barra de escala
    ax.plot([-41.2, -40.4], [-7.5, -7.5], 'k-', linewidth=4)
    ax.plot([-41.2, -41.2], [-7.7, -7.3], 'k-', linewidth=4)
    ax.plot([-40.4, -40.4], [-7.7, -7.3], 'k-', linewidth=4)
    ax.text(-40.8, -8, '~80 km', ha='center', fontsize=11)
    
    # Rosa do vento
    ax.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction', fontsize=16, fontweight='bold')
    ax.annotate('^', xy=(0.97, 0.93), xycoords='axes fraction', fontsize=20, ha='center', color='gray')
    
    # Info
    info = """CRATEUS
- Coordenadas: -5.74°, -40.41°
- IFCE Campus
- Regiao: Sertao do Ceara
- Zona Influencia: ~80km"""
    ax.text(0.02, 0.02, info, transform=ax.transAxes,
           fontsize=10, va='bottom', ha='left',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_detalhe.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa de Crateus salvo")
    
    # HTML interativo
    import folium
    m = folium.Map(location=[crateus_lat, crateus_lon], zoom_start=8)
    folium.Marker([crateus_lat, crateus_lon],
                  popup='<b>IFCE Campus Crateus</b>',
                  icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')).add_to(m)
    folium.Circle([crateus_lat, crateus_lon], radius=40000, color='blue',
                  fill=True, fillOpacity=0.2, popup='Zona de Influencia').add_to(m)
    m.save(f'{OUTPUT_DIR}mapa_crateus_detalhe.html')

def create_interactive_map():
    """Mapa interativo completo"""
    print("Gerando mapa interativo...")
    import folium
    
    m = folium.Map(location=[-10.0, -40.0], zoom_start=5, tiles='CartoDB positron')
    folium.TileLayer('OpenStreetMap').add_to(m)
    
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
                           popup=f'<b>{nome}</b><br>Nordeste').add_to(fg_n)
    
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
    
    print("=" * 60)
    print("  GERACAO COMPLETA DE MAPAS - TESE MCP")
    print("=" * 60)
    
    create_brazil_map()
    create_northeast_map()
    create_ceara_map()
    create_crateus_detail_map()
    create_interactive_map()
    
    print("=" * 60)
    print("  TODOS OS MAPAS GERADOS COM SUCESSO!")
    print("=" * 60)

if __name__ == '__main__':
    main()
