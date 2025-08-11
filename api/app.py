import os
import psutil
import datetime
from flask import Flask, request, jsonify
from typing import Dict, Union

app = Flask(__name__)
vlans: Dict[str, Dict[str, Union[int, str]]] = {}

@app.route('/')
def home():
    """Endpoint raiz que lista todos os endpoints disponíveis"""
    return jsonify({
        "message": "API de Gerenciamento de VLANs",
        "endpoints": {
            "criar_vlan": {"method": "POST", "url": "/vlans"},
            "listar_vlans": {"method": "GET", "url": "/vlans"},
            "consultar_vlan": {"method": "GET", "url": "/vlans/<id>"},
            "healthcheck": {"method": "GET", "url": "/health"}
        }
    }), 200

@app.route('/vlans', methods=['POST'])
def create_vlan():
    """Endpoint para criação de VLANs com validação completa"""
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 415
        
    data = request.get_json()
    
    # Validação do payload
    if 'id' not in data:
        return jsonify({"error": "Campo 'id' é obrigatório"}), 400
        
    try:
        vlan_id = int(data['id'])
    except (ValueError, TypeError):
        return jsonify({"error": "ID deve ser um número inteiro válido"}), 400
    
    # Validação de faixa
    if not (2 <= vlan_id <= 4094):
        return jsonify({
            "error": "ID de VLAN inválido",
            "detalhes": "O padrão IEEE 802.1Q requer IDs entre 2 e 4094"
        }), 400
    
    # Verifica se VLAN já existe
    vlan_key = str(vlan_id)
    if vlan_key in vlans:
        return jsonify({
            "error": "VLAN já existe",
            "vlan_existente": vlans[vlan_key]
        }), 409
    
    # Cria a VLAN
    vlans[vlan_key] = {
        "id": vlan_id,
        "name": data.get('name', f"VLAN_{vlan_id}"),
        "status": "active",
        "created_at": datetime.datetime.now().isoformat()
    }
    
    return jsonify({
        "message": "VLAN criada com sucesso",
        "vlan": vlans[vlan_key],
        "total_vlans": len(vlans)
    }), 201

@app.route('/vlans', methods=['GET'])
def get_all_vlans():
    """Endpoint para listar todas as VLANs"""
    return jsonify({
        "total_vlans": len(vlans),
        "vlans": list(vlans.values())
    }), 200

@app.route('/vlans/<int:vlan_id>', methods=['GET'])
def get_vlan(vlan_id: int):
    """Endpoint para consulta de VLAN específica"""
    vlan_key = str(vlan_id)
    if vlan_key not in vlans:
        return jsonify({"error": f"VLAN {vlan_id} não encontrada"}), 404
    return jsonify(vlans[vlan_key])

@app.route('/health')
def health_check():
    """Endpoint para verificação do status da API"""
    return jsonify({
        "status": "healthy",
        "vlans_registradas": len(vlans),
        "memoria_utilizada": f"{psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.2f}MB",
        "timestamp": datetime.datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)


@app.route('/ui')
def ui_dashboard():
    """Interface web amigável para a API"""
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API de VLANs - Intelbras</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <header class="bg-blue-600 text-white p-6 rounded-lg shadow-lg mb-8">
                <div class="flex items-center">
                    <img src="https://www.intelbras.com/sites/default/files/logo-intelbras.svg" alt="Intelbras" class="h-12 mr-4">
                    <div>
                        <h1 class="text-3xl font-bold">API de Gerenciamento de VLANs</h1>
                        <p class="text-blue-100">Sistema integrado com Java, MikroTik, PED e Smart</p>
                    </div>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Card de Endpoints -->
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h2 class="text-xl font-semibold text-blue-700 mb-4 border-b pb-2">
                        <i class="fas fa-plug mr-2"></i>Endpoints da API
                    </h2>
                    <ul class="space-y-3">
                        <li class="p-3 bg-gray-50 rounded hover:bg-blue-50">
                            <span class="font-medium">GET /</span>
                            <p class="text-sm text-gray-600">Lista endpoints disponíveis</p>
                        </li>
                        <li class="p-3 bg-gray-50 rounded hover:bg-blue-50">
                            <span class="font-medium">POST /vlans</span>
                            <p class="text-sm text-gray-600">Criar nova VLAN</p>
                        </li>
                        <li class="p-3 bg-gray-50 rounded hover:bg-blue-50">
                            <span class="font-medium">GET /vlans</span>
                            <p class="text-sm text-gray-600">Listar todas VLANs</p>
                        </li>
                        <li class="p-3 bg-gray-50 rounded hover:bg-blue-50">
                            <span class="font-medium">GET /vlans/&lt;id&gt;</span>
                            <p class="text-sm text-gray-600">Consultar VLAN específica</p>
                        </li>
                        <li class="p-3 bg-gray-50 rounded hover:bg-blue-50">
                            <span class="font-medium">GET /health</span>
                            <p class="text-sm text-gray-600">Healthcheck do sistema</p>
                        </li>
                    </ul>
                </div>

                <!-- Card de Estatísticas -->
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h2 class="text-xl font-semibold text-blue-700 mb-4 border-b pb-2">
                        <i class="fas fa-chart-bar mr-2"></i>Estatísticas
                    </h2>
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <span>VLANs registradas:</span>
                            <span class="font-bold">{len(vlans)}</span>
                        </div>
                        <div class="flex items-center justify-between">
                            <span>Uso de memória:</span>
                            <span class="font-bold">{psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.2f} MB</span>
                        </div>
                        <div class="pt-4 border-t">
                            <a href="/health" class="text-blue-600 hover:text-blue-800 text-sm">
                                <i class="fas fa-heartbeat mr-1"></i> Ver healthcheck completo
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Card de Tecnologias -->
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h2 class="text-xl font-semibold text-blue-700 mb-4 border-b pb-2">
                        <i class="fas fa-microchip mr-2"></i>Tecnologias Integradas
                    </h2>
                    <ul class="space-y-2">
                        <li class="flex items-center"><i class="fab fa-java text-red-500 mr-2"></i> Java</li>
                        <li class="flex items-center"><i class="fas fa-network-wired text-green-500 mr-2"></i> MikroTik</li>
                        <li class="flex items-center"><i class="fas fa-mobile-alt text-purple-500 mr-2"></i> PED</li>
                        <li class="flex items-center"><i class="fas fa-lightbulb text-yellow-500 mr-2"></i> Smart</li>
                    </ul>
                </div>
            </div>

            <footer class="mt-12 text-center text-gray-500 text-sm">
                <p>© {datetime.datetime.now().year} Intelbras. Todos os direitos reservados.</p>
            </footer>
        </div>
    </body>
    </html>
    """