"""
Mapa Detalhado de Crateus - Versao Melhorada
Tese de Doutorado - MCP e Educacao noertao do Ceara
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'output/mapas/'

def get_brazil_states():
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    return gpd.read_file(url)

def create_crateus_detail_map():
    """Mapa detalhado e melhorado de Crateus"""
    print("Gerando mapa detalhado de Crateus...")
    fig, ax = plt.subplots(1, 1, figsize=(16, 16))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    
    # Fundo com gradiente
    ax.set_facecolor('#F0FFF0')
    
    # === TITULO ===
    ax.set_title('Mapa da Regiao de Crateus - Sertao do Ceara\n(Area de Estudo: IFCE Campus e Municipios do Entorno)',
                fontsize=20, fontweight='bold', pad=25, color='#1a1a1a')
    
    # === ZONAS DE INFLUENCIA (circulos concetricos) ===
    # Zona primaria (30km)
    circle1 = Circle((crateus_lon, crateus_lat), 0.35, fill=True,
                    color='#FF6B6B', alpha=0.15, label='Zona Primaria (30km)')
    ax.add_patch(circle1)
    
    # Zona secundaria (50km)
    circle2 = Circle((crateus_lon, crateus_lat), 0.55, fill=True,
                    color='#4ECDC4', alpha=0.15, label='Zona Secundaria (50km)')
    ax.add_patch(circle2)
    
    # Zona terciaria (80km)
    circle3 = Circle((crateus_lon, crateus_lon), 0.85, fill=True,
                    color='#45B7D1', alpha=0.1, label='Zona Terciaria (80km)')
    ax.add_patch(circle3)
    
    # === IFCE CAMPUS CRATEUS ( Destaque principal) ===
    ax.plot(crateus_lon, crateus_lat, '*', markersize=700, color='#FF0000',
           markeredgecolor='#8B0000', markeredgewidth=3, zorder=15)
    
    # Halo ao redor do IFCE
    halo = Circle((crateus_lon, crateus_lat), 0.15, fill=True,
                 color='#FFD700', alpha=0.4)
    ax.add_patch(halo)
    
    ax.annotate('IFCE - Campus Crateus\n(POLO PRINCIPAL)',
               xy=(crateus_lon, crateus_lat),
               xytext=(crateus_lon - 2.5, crateus_lat + 1.5),
               fontsize=14, fontweight='bold', color='#8B0000',
               arrowprops=dict(arrowstyle='->', color='#8B0000', lw=2.5),
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFFACD',
                       edgecolor='#8B0000', linewidth=3))
    
    # === MUNICIPIOS DO ENTORNO ===
    # Cidades com populacao
    cidades = {
        'Crateus': {'lat': -5.7433, 'lon': -40.4108, 'tipo': 'centro'},
        'Tamboril': {'lat': -4.79, 'lon': -40.82, 'tipo': 'municipio'},
        'Ipueiras': {'lat': -4.35, 'lon': -40.71, 'tipo': 'municipio'},
        'Novo Oriente': {'lat': -5.47, 'lon': -40.74, 'tipo': 'municipio'},
        'Pereiro': {'lat': -5.96, 'lon': -38.47, 'tipo': 'municipio'},
        'Varjota': {'lat': -4.53, 'lon': -40.47, 'tipo': 'municipio'},
        'Santa Quiteria': {'lat': -4.33, 'lon': -40.15, 'tipo': 'municipio'},
        'Senador Pompeu': {'lat': -5.58, 'lon': -39.37, 'tipo': 'municipio'},
        'Quixada': {'lat': -4.97, 'lon': -39.01, 'tipo': 'municipio'},
        'Sobral': {'lat': -3.69, 'lon': -40.37, 'tipo': 'municipio'},
    }
    
    for cidade, dados in cidades.items():
        lat, lon = dados['lat'], dados['lon']
        
        if dados['tipo'] == 'centro':
            continue  # Ja plotado
        
        # Marcadores diferentes por tipo
        if dados['tipo'] == 'municipio':
            ax.plot(lon, lat, 's', markersize=180, color='#228B22',
                   alpha=0.9, markeredgecolor='black', markeredgewidth=1.5, zorder=8)
            ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.3, lat+0.3),
                       fontsize=11, fontweight='bold', color='#006400',
                       arrowprops=dict(arrowstyle='->', color='#228B22', lw=1.5))
    
    # === ESTRADAS (linhas tracejadas) ===
    # Estrada Crateus - Fortaleza
    ax.plot([-40.41, -38.54], [-5.74, -3.71], '--', color='#666666', 
           linewidth=1.5, alpha=0.5, zorder=2)
    
    # Estrada Crateus - Sobral
    ax.plot([-40.41, -40.37], [-5.74, -3.69], '--', color='#666666', 
           linewidth=1.5, alpha=0.5, zorder=2)
    
    # === LEGENDA ===
    legend_elements = [
        plt.Line2D([0], [0], marker='*', color='w', label='IFCE Campus Crateus',
                  markerfacecolor='#FF0000', markersize=25, markeredgecolor='#8B0000', markeredgewidth=2),
        plt.Line2D([0], [0], marker='s', color='w', label='Municipios do Entorno',
                  markerfacecolor='#228B22', markersize=15),
        mpatches.Patch(color='#FF6B6B', alpha=0.3, label='Zona Primaria (30km)'),
        mpatches.Patch(color='#4ECDC4', alpha=0.3, label='Zona Secundaria (50km)'),
        mpatches.Patch(color='#45B7D1', alpha=0.2, label='Zona Terciaria (80km)'),
        plt.Line2D([0], [0], linestyle='--', color='#666666', label='Rodovias')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11,
             framealpha=0.95, title='Legenda', title_fontsize=12)
    
    # === ESCALA E ORIENTACAO ===
    # Barra de escala
    bar_lon = -41.0
    bar_lat = -7.5
    ax.plot([bar_lon, bar_lon + 0.5], [bar_lat, bar_lat], 'k-', linewidth=3)
    ax.plot([bar_lon, bar_lon], [bar_lat - 0.05, bar_lat + 0.05], 'k-', linewidth=3)
    ax.plot([bar_lon + 0.5, bar_lon + 0.5], [bar_lat - 0.05, bar_lat + 0.05], 'k-', linewidth=3)
    ax.text(bar_lon + 0.25, bar_lat - 0.2, '~50 km', ha='center', fontsize=10)
    
    # Rosa do vento (N)
    ax.annotate('N', xy=(0.97, 0.97), xycoords='axes fraction',
               fontsize=16, fontweight='bold', ha='center')
    ax.annotate('^', xy=(0.97, 0.93), xycoords='axes fraction',
               fontsize=20, ha='center', color='gray')
    
    # === CONFIGURACOES DO EIXO ===
    ax.set_xlim(-42.5, -37)
    ax.set_ylim(-8, -3)
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.4, color='gray')
    
    # === CAIXA DE INFORMACOES ===
    info_text = """IFCE Campus Crateus
- Localizacao: -5.74, -40.41
- Regiao: Sertao do Ceara
- Area de Influencia: ~80km"""
    ax.text(0.98, 0.02, info_text, transform=ax.transAxes,
           fontsize=9, va='bottom', ha='right',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_detalhe.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("[OK] Mapa detalhado de Crateus salvo")

def create_ceara_improved():
    """Mapa do Ceara melhorado com mais detalhes"""
    print("Gerando mapa do Ceara melhorado...")
    fig, ax = plt.subplots(1, 1, figsize=(18, 16))
    
    states = get_brazil_states()
    states = states.to_crs(epsg=4326)
    
    # Plotar Ceara
    ceara = states[states['sigla'] == 'CE']
    gpd.GeoSeries(ceara.geometry.values).plot(ax=ax, facecolor='#FFB347', 
                                                   edgecolor='black', linewidth=3)
    
    # Plotar estados vizinhos com cores diferentes
    vizinhos = states[states['sigla'].isin(['PI', 'RN', 'PB', 'CE'])]
    if len(vizinhos) > 0:
        gpd.GeoSeries(vizinhos[vizinhos['sigla'] != 'CE'].geometry.values).plot(
            ax=ax, facecolor='#E8E8E8', edgecolor='gray', linewidth=1)
    
    # Centro do Ceara
    ceara_geom = ceara.geometry.iloc[0]
    centroid = ceara_geom.centroid
    ax.annotate('CEARA', xy=(centroid.x, centroid.y),
               fontsize=30, ha='center', va='center',
               fontweight='bold', color='white',
               path_effects=[path_effects.withStroke(linewidth=5, foreground='#CC7700')])
    
    # Principais cidades do Ceara
    cidades_ceara = {
        'Fortaleza': (-3.71, -38.54, 2500000),
        'Crateus': (-5.7433, -40.4108, 75000),
        'Sobral': (-3.69, -40.37, 200000),
        'Juazeiro do Norte': (-7.21, -39.30, 250000),
        'Quixada': (-4.97, -39.01, 83000),
        'Iguatu': (-6.24, -39.30, 100000),
        'Cascavel': (-3.97, -38.24, 120000),
        'Pacajus': (-4.04, -38.08, 70000),
    }
    
    for cidade, (lat, lon, pop) in cidades_ceara.items():
        # Tamanho proporcional a populacao
        size = min(max(pop / 10000, 100), 400)
        
        if cidade == 'Crateus':
            # Destaque especial para Crateus
            ax.plot(lon, lat, '*', markersize=500, color='red',
                   markeredgecolor='darkred', markeredgewidth=3, zorder=10)
            ax.annotate(f'{cidade}\n(IFCE)', xy=(lon, lat),
                       xytext=(lon + 1.2, lat + 0.8),
                       fontsize=12, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='red', lw=2),
                       bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
        else:
            ax.plot(lon, lat, 'o', markersize=size/15, color='#333333',
                   alpha=0.8, markeredgecolor='black', zorder=5)
            ax.annotate(cidade, xy=(lon, lat), xytext=(lon+0.3, lat+0.3),
                       fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax.set_xlim(-42.5, -36.5)
    ax.set_ylim(-8.5, -2.5)
    ax.set_title('Mapa do Estado do Ceara\nCom Principais Cidades e Destaque para Crateus',
                fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_facecolor('#FFF8DC')
    
    # Legenda
    legend = [
        mpatches.Patch(color='#FFB347', label='Ceara'),
        mpatches.Patch(color='#E8E8E8', label='Estados Vizinhos'),
        plt.Line2D([0], [0], marker='*', color='w', label='IFCE Crateus',
                  markerfacecolor='red', markersize=20, markeredgecolor='darkred'),
    ]
    ax.legend(handles=legend, loc='lower right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_ceara_crateus.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa do Ceara salvo")

def create_crateus_zoom():
    """Mapa com zoom extra em Crateus"""
    print("Gerando mapa com zoom em Crateus...")
    fig, ax = plt.subplots(1, 1, figsize=(14, 14))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    
    ax.set_facecolor('#E8FFE8')
    
    # Regiao retangular ao redor de Crateus
    from matplotlib.patches import Rectangle
    regiao = Rectangle((-41.5, -6.5), 2.5, 2, fill=False, 
                       edgecolor='gray', linestyle='--', linewidth=2)
    ax.add_patch(regiao)
    
    # IFCE com efeito de brilho
    for i in range(3):
        size = 250 + i * 100
        alpha = 0.3 - i * 0.1
        ax.plot(crateus_lon, crateus_lat, '*', markersize=size, color='yellow',
               alpha=alpha, zorder=5)
    
    # IFCE principal
    ax.plot(crateus_lon, crateus_lat, '*', markersize=500, color='#FF0000',
           markeredgecolor='#8B0000', markeredgewidth=3, zorder=10)
    
    ax.annotate('IFCE CAMPUS CRATEUS\n(Instituicao Federal)',
               xy=(crateus_lon, crateus_lat),
               xytext=(crateus_lon - 1.5, crateus_lat + 0.8),
               fontsize=13, fontweight='bold', color='#8B0000',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFF00',
                       edgecolor='#FF0000', linewidth=2))
    
    # Municipios proximos
    municipios = {
        'Tamboril': (-4.79, -40.82),
        'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74),
        'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47),
    }
    
    for nome, (lat, lon) in municipios.items():
        ax.plot(lon, lat, 'o', markersize=120, color='#006400',
               alpha=0.9, markeredgecolor='black', zorder=5)
        ax.annotate(nome, xy=(lon, lat), xytext=(lon+0.2, lat+0.2),
                   fontsize=11, fontweight='bold', color='#006400',
                   arrowprops=dict(arrowstyle='->', color='#006400'))
    
    ax.set_xlim(-41.8, -38.5)
    ax.set_ylim(-7, -4)
    ax.set_title('Zoom: Regiao de Crateus - Sertao do Ceara\n(Polo Educacional)',
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_zoom.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa com zoom salvo")

def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 55)
    print("  MAPAS MELHORADOS DE CRATEUS")
    print("=" * 55)
    
    create_crateus_detail_map()
    create_ceara_improved()
    create_crateus_zoom()
    
    print("=" * 55)
    print("  MAPAS GERADOS!")
    print("=" * 55)

if __name__ == '__main__':
    main()
