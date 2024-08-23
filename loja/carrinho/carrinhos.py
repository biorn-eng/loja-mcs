from flask import redirect, request, session, url_for, flash, current_app, jsonify
from loja import app, db
from loja.produtos.models import Addproduto
from flask import Flask, render_template
from loja.produtos.rotas import marcas, categorias
import json
from flask import request, redirect, url_for, flash
from loja import app, db
from loja.produtos.models import *
from loja.clientes.model import ClientePedido
from flask_login import login_required, current_user, login_user, logout_user

def M_Dicionarios(dic1, dic2):
    if isinstance(dic1, list) and isinstance(dic2, list):
        return dic1 + dic2
    elif isinstance(dic1, dict) and isinstance(dic2, dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        produto_id = request.form.get('produto_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('color')
        tamanho = request.form.get('tamanho') 
        produto = Addproduto.query.get(produto_id)

        if produto:
            if produto.stock >= quantity:
                DicItems = {
                    'id': produto.id,
                    'name': produto.name,
                    'price': produto.price,
                    'discount': produto.discount,
                    'color': color,
                    'tamanho': tamanho,
                    'quantity': quantity,
                    'image': produto.image_1
                }

                if 'LojainCarrinho' not in session:
                    session['LojainCarrinho'] = {}

                carrinho = session['LojainCarrinho']

                if produto_id in carrinho:
                    carrinho[produto_id]['quantity'] += quantity
                else:
                    carrinho[produto_id] = DicItems

                session['LojainCarrinho'] = carrinho
                # Recalcular o frete se o carrinho não estiver vazio
                if not session['LojainCarrinho']:
                    session.pop('valor_frete', None)
                    
                return redirect(request.referrer)
            else:
                flash(f"Estoque insuficiente. Apenas {produto.stock} unidades disponíveis.", 'warning')
                return redirect(request.referrer)
        else:
            flash("Produto não encontrado.", 'danger')
            return redirect(request.referrer)
    except Exception as e:
        print(f"Erro ao adicionar ao carrinho: {e}")
        flash("Ocorreu um erro ao adicionar o produto ao carrinho.", 'danger')
        return redirect(request.referrer)



@app.route('/carros')
def getCart():
    if 'LojainCarrinho' not in session:
        return redirect(request.referrer)
    
    carrinho = session['LojainCarrinho']
    
    # Zerar o frete quando o carrinho ou a página é carregada
    session.pop('valor_frete', None)
    session.pop('servico_frete', None)
    session.pop('prazo_frete', None)
    
    for key, produto in carrinho.items():
        produto_db = Addproduto.query.get(key)
        if produto_db:
            produto['available_colors'] = ",".join(produto_db.color.split(","))
            produto['available_tamanhos'] = ",".join(produto_db.tamanho.split(","))
            produto['selected_color'] = produto.get('color', produto_db.color.split(",")[0])
            produto['selected_tamanho'] = produto.get('tamanho', produto_db.tamanho.split(",")[0])
    
    session['LojainCarrinho'] = carrinho

    subtotal = 0
    valorpagar = 0    
    for key, produto in carrinho.items():
        quantity = produto.get('quantity')
        if quantity is not None:
            total_price = float(produto['price']) * int(quantity)
            discount = (produto['discount'] / 100) * total_price
            subtotal += total_price - discount
    imposto = "%.2f" % (.06 * float(subtotal))
    valorpagar = float("%.2f" % (1.06 * subtotal))
    
    frete = session.get('valor_frete', 0.0)
    valorpagar += float(frete)

    return render_template('produtos/carros.html', imposto=imposto, valorpagar=valorpagar, frete=frete)



@app.route('/updateCarro/<int:code>', methods=["POST"])
def updateCarro(code):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))

    if request.method == "POST":
        quantity = int(request.form.get('quantity'))
        color = request.form.get('color')
        tamanho = request.form.get('tamanho')

        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    produto = Addproduto.query.get(code)
                    if produto:
                        if produto.stock >= quantity:
                            item['quantity'] = quantity
                            item['color'] = color
                            item['tamanho'] = tamanho

                            # Zerar o frete ao atualizar o carrinho
                            session.pop('valor_frete', None)
                            session.pop('servico_frete', None)
                            session.pop('prazo_frete', None)

                            flash('Seu carrinho foi atualizado', 'success')
                        else:
                            flash(f"Estoque insuficiente. Apenas {produto.stock} unidades disponíveis.", 'danger')
                    else:
                        flash('Produto não encontrado', 'danger')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            flash('Erro ao atualizar o carrinho', 'danger')
            return redirect(url_for('getCart'))


            




@app.route('/vazio')
def vazio_Cart():
    try:
        session.pop('valor_frete', None)  # Remove o valor do frete
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))
    
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            if int(key) == id:
                session['LojainCarrinho'].pop(key, None) # Remove o valor do frete
                session.pop('valor_frete', None)
                flash('Seu carrinho foi atualizado')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
    
@app.route('/limparcarro')
def limparcarro():
    try:
        session.pop('LojainCarrinho', None)        
        return redirect(url_for('home'))
    except Exception as e:
        print(e)



@app.route('/salvar_frete', methods=['POST'])
def salvar_frete():
    if current_user.is_authenticated:
        valor_frete = request.json.get('valor_frete')
        servico_frete = request.json.get('servico_frete')
        prazo_frete = request.json.get('prazo_frete')

        session['valor_frete'] = valor_frete
        session['servico_frete'] = servico_frete
        session['prazo_frete'] = prazo_frete

        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

