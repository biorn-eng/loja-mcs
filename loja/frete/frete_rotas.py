import requests
from flask import request, jsonify
from loja import app, db

API_URL = 'https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTYiLCJqdGkiOiJiZjM5ODdlOTMwNTJjY2Y3ZjNhYzgxZGI1ZjE0OWFmNzEzMmQ2NjAxNTdlYjkyMGRkZTEyN2I5NjYwOWFiNDAzYjhjZDA4YjFlMTY2Y2ZmZiIsImlhdCI6MTcyMzkxMDY2Ny4wNTcwMiwibmJmIjoxNzIzOTEwNjY3LjA1NzAyMywiZXhwIjoxNzU1NDQ2NjY3LjAzNjk3NCwic3ViIjoiOWM5ZjliZGItNzUxZi00NTEzLWJlNDctNmM5YTFlYTQwM2Q2Iiwic2NvcGVzIjpbInNoaXBwaW5nLWNhbGN1bGF0ZSJdfQ.TWlZePpakRgCVkX9tCezBLZseAJCS6l4PupYqHb__dIvABevvnE0_0K7o2NH0Z5bsiWlktTt-7QFl5fK6wlgUcwZY8YoE9vVV49h3Da61fTAngxQh47pzODnR8Z7LUXNeDfaHrox084KDGnvYiKxozXBak3UR6bMnbacUh3vv45KoaXsv_r28A_B1OlXBfMp7orWHI5EPWFeZEJTKtrEJg-FJZxg64-jhA3sAUb2Jxd3dpV2I-8DgIdMu183e2M1AbDiy8VbNTDa9kg2GciQJfN8SZ4y82ua5J3xiDfFBNwfQxeOAELEuF0rrsigR0il2Ys31JjdzLjao5MoJZF8fGTsow-mFnul0IKMpocxHpJJkJAwYxbi8JUDpuAYFaINkGdlhEwQKOyGsq89ZaofJ4cew6FVEPqdQx9gJj8oSD_-ASGXIdLogxnHN09dDTD1VS7psANjwkvgheoKig3m4ODRIbla0UG6JYdE6iiOrmRIX2rQoRlWV4CSw9Dh6FKpniAHIshj3sY6TIPTdiD3h46Evj4aJjqOQ0vTJ6s1XNJhaEcJ60kpjsguQoZQWzOYtH_MJzmCeJqObtFLNIvUBWa0xqwu_NkBNpCNhkkk8lP65_AcYCIsFO7E38QJfbxThCWwzahCJHCf6E8cYiD3tGRF6kqIRCYlY4axBRULg8I'

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

    if response.status_code == 200:
        fretes = response.json()
        return jsonify(fretes)
    else:
        return jsonify({"error": "Erro ao calcular frete"}), 500
