import requests
from flask import request, jsonify
from loja import app, db

API_URL = 'https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTYiLCJqdGkiOiI4YWQ2NTY1ZjRiZjRjMmYyZjgyNDdjOTc0NDI4MTFjY2RhYjdiNDBmZWY1MjdhODc5NjQ4MDM0NDg3NTFhNDUzZGFkMTUwNDQzOGM0NDUyZiIsImlhdCI6MTc4MjE2MDMxOS4yOTQzNzEsIm5iZiI6MTc4MjE2MDMxOS4yOTQzNzQsImV4cCI6MTgxMzY5NjMxOS4yODUwOTYsInN1YiI6IjljOWY5YmRiLTc1MWYtNDUxMy1iZTQ3LTZjOWExZWE0MDNkNiIsInNjb3BlcyI6WyJjYXJ0LXJlYWQiLCJjYXJ0LXdyaXRlIiwiY29tcGFuaWVzLXJlYWQiLCJjb21wYW5pZXMtd3JpdGUiLCJjb3Vwb25zLXJlYWQiLCJjb3Vwb25zLXdyaXRlIiwibm90aWZpY2F0aW9ucy1yZWFkIiwib3JkZXJzLXJlYWQiLCJwcm9kdWN0cy1yZWFkIiwicHJvZHVjdHMtZGVzdHJveSIsInByb2R1Y3RzLXdyaXRlIiwicHVyY2hhc2VzLXJlYWQiLCJzaGlwcGluZy1jYWxjdWxhdGUiLCJzaGlwcGluZy1jYW5jZWwiLCJzaGlwcGluZy1jaGVja291dCIsInNoaXBwaW5nLWNvbXBhbmllcyIsInNoaXBwaW5nLWdlbmVyYXRlIiwic2hpcHBpbmctcHJldmlldyIsInNoaXBwaW5nLXByaW50Iiwic2hpcHBpbmctc2hhcmUiLCJzaGlwcGluZy10cmFja2luZyIsImVjb21tZXJjZS1zaGlwcGluZyIsInRyYW5zYWN0aW9ucy1yZWFkIiwidXNlcnMtcmVhZCIsInVzZXJzLXdyaXRlIiwid2ViaG9va3MtcmVhZCIsIndlYmhvb2tzLXdyaXRlIiwid2ViaG9va3MtZGVsZXRlIiwidGRlYWxlci13ZWJob29rIl19.CHhIEIzwNv2gpiAitlgL9gkbxjOzLAtNlALNjL-3KBejRbe5qtcxP4IlG152c3cvWLaW5PG1CV6HPFF3U8R9KwhhuEgQUucUbD7XCeNGjbK_S0_MOlgnSMzPVUjBV8YFkBdh5JtYE12DRZMb8k6BfH46tsDBx8_jJK6tUXzr2LLbVWMoh-O8ka16__qXhagSxMOzoLMl_zsqqBWmq5_MepJZXBN2cFMQPBZy1YRKLau_OIrvhFT7K-d6Buh9q1NmIpfVjQGIZ60b689j6sE3CBks1xfrduaISunUUpH1B_rlzdcDcQy0jmVq57sHtaQMcyWKZEfO5IClB6EFmuM086S4lZNO4gnI1iUKoWX27njVK5dNH2WfmWMBigCE0HcTrY2Ad4HYFHddD95WOzueBLWzABJUX-hr6VKHaPdMsJmUUOzO1T3t0Kd1tumm3mig8x1G4cV5QZwf91cX8e32fe4REzv-JlYraMuJqHy4uyUjviUsqVMTz8RgkPny0Tx07WVnZyN4XtgvhqgWIcG_3NfsLw6BjMP9wvAH4ZgylJeuA5YYsDRDEqGQY2fKoepTfzX6CDONX9_rMa-cAClGr1L1IqfrtkyDBQ-UzgDP0C4tK4bUeMmPZrc_CTI5Xp3rcO-maYF6MiW9nvFEzKanhHQ9w8Z2FRk-r8BIKtuRLvw'

@app.route('/calcular_frete', methods=['POST'])
def calcular_frete():
    cep_destino = request.json.get('cep_destino')

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "from": {
            "postal_code": "88135420"  # CEP de origem
        },
        "to": {
            "postal_code": cep_destino  # CEP de destino fornecido pelo cliente
        },
        "products": [
            {
                "weight": 0.2,  # Peso do produto
                "width": 5,  # Largura do produto
                "height": 5,  # Altura do produto
                "length": 5,  # Comprimento do produto
                "insurance_value": 1  # Valor do seguro
            }
        ],
        "services": "1,2"  # 1 para Correios, 2 para Jadlog
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print("STATUS:", response.status_code)
    print("RESPOSTA:")
    print(response.text)

    if response.status_code == 200:
      fretes = response.json()
      return jsonify(fretes)
    else:
        print("ERRO API:")
        print("STATUS:", response.status_code)
        print(response.text[:1000])

    return jsonify({
        "error": "Erro ao calcular frete",
        "status": response.status_code
    }), 500
