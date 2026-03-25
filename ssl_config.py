
# Configuração SSL para MASWOS V5 NEXUS
import urllib3
import ssl

# Desativar verificações SSL para APIs governamentais
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurar contexto SSL mais permissivo para APIs específicas
ssl._create_default_https_context = ssl._create_unverified_context
