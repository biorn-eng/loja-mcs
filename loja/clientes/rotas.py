from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response, jsonify
from flask_bcrypt import Bcrypt
from loja import db, app, bcrypt, login_manager
from.forms import CadastroClienteForm, ClienteLoginForm
import secrets, os
from.model import Cadastrar, ClientePedido
from flask_login import login_required, current_user, login_user, logout_user
import pdfkit
from .forms import CadastroClienteForm, ClienteLoginForm, AtualizaClienteForm
import mercadopago
from loja.produtos.models import Addproduto




# Configurar Mercado Pago
mp = mercadopago.SDK("APP_USR-3222709748226137-073111-303977dedccdae1a0ff9493a50ee0374-1923594057")

@app.route('/pagamento', methods=['POST'])
@login_required
def pagamento():
    notafiscal = request.form.get('invoice')
    amount = request.form.get('amount')

    # Inclui o valor do frete no total
    frete = session.get('valor_frete', 0.0)
    total_amount = float(amount) + frete
    
    preference_data = {
        "items": [
            {
                "title": "loja materiais de construção do shape",
                "quantity": 1,
                "unit_price": total_amount / 100,  # Valor total dividido por 100 para centavos
                "currency_id": "BRL"
            }
        ],
        "back_urls": {
            "success": url_for('obrigado', _external=True, total_amount=total_amount),  # Inclui o total pago como parâmetro
            "failure": url_for('pagamento_erro', _external=True),
            "pending": url_for('pagamento_pendente', _external=True)
        },
        "auto_return": "approved",
        "external_reference": notafiscal
    }

    preference = mp.preference().create(preference_data)
    preference_id = preference['response']['id']

    return redirect(preference['response']['init_point'])




@app.route('/obrigado')
def obrigado():
    notafiscal = request.args.get('external_reference')
    cliente_pedido = ClientePedido.query.filter_by(cliente_id=current_user.id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
    if cliente_pedido:
        cliente_pedido.status = 'pago'
        total_amount = request.args.get('total_amount', type=float)  # Obtém o valor total pago
        cliente_pedido.total_pago = total_amount / 100
        db.session.commit()
    return render_template('cliente/obrigado.html')





@app.route('/pagamento_erro')
def pagamento_erro():
    return render_template('cliente/pagamento_erro.html')

@app.route('/pagamento_pendente')
def pagamento_pendente():
    notafiscal = request.args.get('external_reference')  # Ajuste para pegar o parâmetro correto
    # Você pode adicionar lógica aqui se desejar lidar com pedidos pendentes de forma específica
    return render_template('cliente/pagamento_pendente.html')



@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = CadastroClienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, country=form.country.data, state=form.state.data, city=form.city.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(cadastrar)
        flash(f'Obrigado {form.name.data} por se cadastrar', 'success')
        db.session.commit()
        return redirect(url_for('clientelogin'))
    return render_template('cliente/cliente.html', form=form)

@app.route('/cliente/login', methods=['GET', 'POST'])
def clientelogin():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        print(f'Usuário encontrado: {user}')  # linha para depuração
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            print(f'Usuário logado: {current_user}')  # linha para depuração
            flash('Login realizado com sucesso', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Senha e email incorretos', 'danger')
        return redirect(url_for('clientelogin'))
    return render_template('cliente/login.html', form=form)

@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        
        # Verifica se o valor do frete está presente na sessão
        if 'valor_frete' not in session:
            flash('Você precisa selecionar uma opção de frete antes de finalizar a compra.', 'danger')
            return redirect(url_for('getCart'))

        try:
            gTotal = 0
            frete = session.get('valor_frete', 0.0)  # Recupera o valor do frete da sessão

            for item in session['LojainCarrinho'].values():
                desconto = (item['discount'] / 100) * float(item['price'])
                subTotal = float(item['price']) * int(item['quantity'])
                subTotal -= desconto
                gTotal += subTotal

                produto = Addproduto.query.get(item['id'])
                if produto.stock >= item['quantity']:
                    produto.stock -= item['quantity']
                else:
                    flash(f'Estoque insuficiente para o produto {produto.name}', 'danger')
                    return redirect(url_for('getCart'))

            gTotal = float("%.2f" % (1.06 * gTotal))  # Inclui imposto
            gTotal += frete  # Adiciona o valor do frete ao total

            p_order = ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'], total_pago=gTotal)
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            session.pop('valor_frete', None)  # Remove o valor do frete após o pedido ser realizado
            flash('Seu pedido foi gerado com sucesso', 'success')
            return redirect(url_for('pedidos', notafiscal=notafiscal))
        except Exception as e:
            print(e)
            flash('Não foi possível processar seu pedido', 'danger')
            return redirect(url_for('getCart'))









@app.route('/pedidos/<notafiscal>')
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        cliente = Cadastrar.query.filter_by(id=cliente_id).first()
        pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
        for _key, produto in pedidos.pedido.items():
            desconto = (produto['discount']/100) * float(produto['price'])
            subTotal += float(produto['price']) * int(produto['quantity'])
            subTotal -= desconto
            imposto = ("%.2f" %(.06 * float(subTotal)))
            gTotal = float("%.2f" %(1.06 * subTotal))
        frete = pedidos.total_pago - gTotal  # Assumindo que o total_pago já inclui o frete
        gTotal += frete
    else:
        return redirect(url_for('clientelogin'))
    return render_template('cliente/pedido.html', notafiscal=notafiscal, imposto=imposto, subTotal=subTotal, gTotal=gTotal, cliente=cliente, pedidos=pedidos, frete=frete, discount=desconto )


@app.route('/get_pdf/<notafiscal>', methods=['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        if request.method == "POST":
            cliente = Cadastrar.query.filter_by(id=cliente_id).first()
            pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key, produto in pedidos.pedido.items():
                desconto = (produto['discount']/100) * float(produto['price'])
                subTotal += float(produto['price']) * int(produto['quantity'])
                subTotal -= desconto
                imposto = ("%.2f" %(.06 * float(subTotal)))
                gTotal = float("%.2f" %(1.06 * subTotal))
            frete = pedidos.total_pago - gTotal  # Assumindo que o total_pago já inclui o frete
            gTotal += frete

            rendered = render_template('cliente/pdf.html', notafiscal=notafiscal, imposto=imposto, subTotal=subTotal, gTotal=gTotal, cliente=cliente, pedidos=pedidos, frete=frete)
            
            # Configurando o caminho para o wkhtmltopdf
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=' + notafiscal + '.pdf'
            return response
    return redirect(url_for('pedidos'))





#PAGINA DO CLIENTE

@app.route('/cliente/paginadocliente', methods=['GET'])
@login_required
def paginadocliente():
    # Página inicial do cliente
    return render_template('cliente/paginadocliente.html')

@app.route('/cliente/pedidos', methods=['GET'])
@login_required
def pedidos_cliente():
    # Página com a tabela de pedidos
    cliente = Cadastrar.query.get(current_user.id)
    pedidos = ClientePedido.query.filter_by(cliente_id=cliente.id).all()
    pedidos_com_clientes = []

    for pedido in pedidos:
        pedidos_com_clientes.append({
            'pedido': pedido,
            'cliente': cliente
        })

    return render_template('cliente/pedidos_cliente.html', pedidos=pedidos_com_clientes)

@app.route('/cliente/pedidos/<int:pedido_id>')
@login_required
def suascompras(pedido_id):
    pedido = ClientePedido.query.get_or_404(pedido_id)
    cliente = Cadastrar.query.get(pedido.cliente_id)
    produtos = pedido.pedido  # Supondo que `pedido.pedido` é um dicionário de produtos

    return render_template('cliente/suascompras.html', pedido=pedido, cliente=cliente, produtos=produtos)



@app.route('/cliente/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_cliente():
    form = AtualizaClienteForm()
    cliente = Cadastrar.query.get(current_user.id)

    if form.validate_on_submit():
        cliente.name = form.name.data
        cliente.username = form.username.data
        cliente.email = form.email.data
        cliente.country = form.country.data
        cliente.state = form.state.data
        cliente.city = form.city.data
        cliente.contact = form.contact.data
        cliente.address = form.address.data
        cliente.zipcode = form.zipcode.data
        db.session.commit()
        flash('Suas informações foram atualizadas com sucesso!', 'success')
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form.name.data = cliente.name
        form.username.data = cliente.username
        form.email.data = cliente.email
        form.country.data = cliente.country
        form.state.data = cliente.state
        form.city.data = cliente.city
        form.contact.data = cliente.contact
        form.address.data = cliente.address
        form.zipcode.data = cliente.zipcode

    return render_template('cliente/atualizar_cliente.html', form=form)




