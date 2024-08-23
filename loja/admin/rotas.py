from flask import render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Addproduto, Marca, Categoria
from loja import app, db, bcrypt
from loja.admin.forms import RegistrationForm, LoginFormulario
from loja.admin.models import User
from loja.clientes.model import ClientePedido, Cadastrar
import json



@app.route('/admin')
def admin():
    if'email' not in session:
        flash('Favor fazer seu login', 'danger')
        return redirect(url_for('login'))
    produtos = Addproduto.query.all()
    return render_template('admin/index.html', title='Pagina Administrativa', produtos=produtos)

@app.route('/marcas')
def marcas():
    if'email' not in session:
        flash('Favor fazer seu login', 'danger')
        return redirect(url_for('login'))
    marcas = Marca.query.order_by(Marca.id.desc()).all()
    return render_template('admin/marca.html', title='Pagina Marcas', marcas=marcas)

@app.route('/categoria')
def categoria():
    if'email' not in session:
        flash('Favor fazer seu login', 'danger')
        return redirect(url_for('login'))
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template('admin/marca.html', title='Pagina Categorias', categorias=categorias)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por se registrar', 'success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Pagina de Registros")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash('Login realizado com sucesso', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('admin/login.html', form=form, title='Pagina Login')

@app.route('/admin/pedidos')
def visualizar_pedidos():
    pedidos = ClientePedido.query.all()
    pedidos_com_clientes = []
    total_pedidos = 0  # Inicializando a variável para armazenar o valor total dos pedidos

    for pedido in pedidos:
        cliente = Cadastrar.query.get(pedido.cliente_id)
        total_pedido_atual = pedido.total_pago if pedido.total_pago is not None else 0  # Tratando None como zero
        total_pedidos += total_pedido_atual  # Somando o total de cada pedido
        pedidos_com_clientes.append({
            'pedido': pedido,
            'cliente': cliente
        })

    return render_template('admin/pedidos.html', pedidos=pedidos_com_clientes, total_pedidos=total_pedidos)




@app.route('/admin/pedido/<int:pedido_id>')
def detalhes_pedido(pedido_id):
    pedido = ClientePedido.query.get_or_404(pedido_id)
    cliente = Cadastrar.query.get(pedido.cliente_id)  # Ajuste se necessário

    # `pedido.pedido` já é um dicionário, então não precisa usar json.loads
    produtos = pedido.pedido  # Diretamente um dicionário de produtos

    return render_template(
        'admin/detalhes_pedido.html',
        pedido=pedido,
        cliente=cliente,
        produtos=produtos
    )




@app.route('/admin/pedido/<int:pedido_id>/atualizar', methods=['POST'])
def atualizar_status(pedido_id):
    pedido = ClientePedido.query.get_or_404(pedido_id)
    novo_status = request.form.get('status')
    pedido.status = novo_status
    db.session.commit()
    flash('Status do pedido atualizado com sucesso!')
    return redirect(url_for('visualizar_pedidos', pedido_id=pedido_id))


