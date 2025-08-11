from flask import Flask, request, jsonify

app = Flask(__name__)
vlans = {}

@app.route('/health')
def health():
    """Endpoint mínimo para healthcheck"""
    return '', 200  # Resposta vazia (mais rápida)

@app.route('/vlans', methods=['GET'])
def get_all_vlans():
    """Endpoint para listar todas as VLANs"""
    return jsonify({
        "count": len(vlans),
        "vlans": list(vlans.values())
    })

@app.route('/vlans', methods=['POST'])
def create_vlan():
    data = request.get_json()
    
    # Validação simplificada mas eficiente
    vlan_id = str(data.get('id'))
    if not vlan_id.isdigit() or not (1 <= int(vlan_id) <= 4094):
        return jsonify({"error": "ID de VLAN inválido"}), 400
        
    vlans[vlan_id] = data
    return jsonify({"id": vlan_id, "status": "active"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)