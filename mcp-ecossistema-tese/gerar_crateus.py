"""
Mapa Específico de Crateús - Versão Profissional
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'output/mapas/'

def create_crateus_only():
    """Mapa dedicado de Crateus"""
    print("Gerando mapa de Crateus...")
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    
    ax.set_facecolor('#F5F5F5')
    
    # IFCE marker
    ax.plot(crateus_lon, crateus_lat, 'o', markersize=12, color='#FF0000', 
           markeredgecolor='#8B0000', markeredgewidth=2, zorder=10)
    ax.annotate('IFCE Campus Crateus', xy=(crateus_lon, crateus_lat),
               xytext=(0.8, 0.5), textcoords='offset points',
               fontsize=12, fontweight='bold', color='#8B0000',
               arrowprops=dict(arrowstyle='->', color='#8B0000', lw=2))
    
    # Cidades do entorno
    cidades = {
        'Tamboril': (-4.79, -40.82),
        'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74),
        'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47),
        'Santa Quiteria': (-4.33, -40.15),
        'Sobral': (-3.69, -40.37),
        'Quixada': (-4.97, -39.01)
    }
    
    for cidade, (lat, lon) in cidades.items():
        ax.plot(lon, lat, 'o', markersize=8, color='#228B22', 
               markeredgecolor='black', zorder=5)
        ax.annotate(cidade, xy=(lon, lat), xytext=(0.3, 0.3), 
                   textcoords='offset points', fontsize=9,
                   arrowprops=dict(arrowstyle='->', color='#228B22'))
    
    # Zona de influência
    circle = plt.Circle((crateus_lon, crateus_lat), 0.6, fill=False,
                        color='blue', linestyle='--', linewidth=2)
    ax.add_patch(circle)
    ax.annotate('Zona de Influencia', xy=(crateus_lon + 0.7, crateus_lat - 0.3),
               fontsize=10, color='blue')
    
    ax.set_title('Mapa de Localização: IFCE Campus Crateus\n(Sertão do Ceará)', 
                fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_xlim(-41.5, -38)
    ax.set_ylim(-7, -3.5)
    ax.grid(True, linestyle='--', alpha=0.4)
    
    # Legenda
    legend = [
        plt.Line2D([0], [0], marker='o', color='w', label='IFCE Campus Crateus',
                  markerfacecolor='#FF0000', markersize=10, markeredgecolor='#8B0000'),
        plt.Line2D([0], [0], marker='o', color='w', label='Municipios',
                  markerfacecolor='#228B22', markersize=8),
    ]
    ax.legend(handles=legend, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_local.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] Mapa de Crateus salvo")

def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_crateus_only()

if __name__ == '__main__':
    main()
