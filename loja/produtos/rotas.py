from flask import redirect, render_template, url_for, flash, request, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto, Avaliacao
import secrets, os
from flask_login import login_required, current_user
from loja.clientes.model import ClientePedido

def marcas():
    marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
    return marcas

def categorias():
    categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
    return categorias


# PAGINA HOME
@app.route('/')
def home():
    pagina = request.args.get('pagina', 1, type=int)    
    # Ordena primeiro pelos produtos esgotados (stock = 0) no final e depois pelo ID decrescente (mais novos primeiro)
    produtos = Addproduto.query.order_by(Addproduto.stock == 0, Addproduto.id.desc()).paginate(page=pagina, per_page=12)    
    print(f"Página atual: {pagina}, Total de produtos na página: {len(produtos.items)}")
    return render_template('produtos/index.html', produtos=produtos, marcas=marcas(), categorias=categorias())





@app.route('/search', methods=['GET', 'POST'])
def search():
    pagina = request.args.get('pagina', 1, type=int)  # Obtém o número da página da query string, padrão 1

    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        produtos = Addproduto.query.filter(Addproduto.name.like(search)).paginate(page=pagina, per_page=4)
        return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias())
    
    elif request.method == 'GET':
        search_value = request.args.get('search_string', '')
        search = "%{0}%".format(search_value)
        produtos = Addproduto.query.filter(Addproduto.name.like(search)).paginate(page=pagina, per_page=4)
        return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias())




@app.route('/marca/<int:id>')
def get_marca(id):
    pagina = request.args.get('pagina', 1, type=int)
    get_m = Marca.query.get_or_404(id)
    marca = Addproduto.query.filter_by(marca_id=get_m.id).paginate(page=pagina, per_page=12)
    print(f"Total de produtos da marca {get_m.id}: {len(marca.items)}")
    return render_template('/produtos/index.html', marca=marca, marcas=marcas(), categorias=categorias(), get_m=get_m)



@app.route('/produto/<int:id>')
def pagina_unica(id):
    produto = Addproduto.query.get_or_404(id)
    avaliacoes = Avaliacao.query.filter_by(produto_id=id).all()
    
    # Verifica se o produto está esgotado
    if produto.stock == 0:
        flash('Este produto está esgotado.', 'warning')
    
    return render_template('produtos/pagina_unica.html', produto=produto, avaliacoes=avaliacoes, marcas=marcas(), categorias=categorias())

@app.route('/produto/<int:id>')
def carros(id):
    produto = Addproduto.query.get_or_404(id)
    
    # Verifica se o produto está esgotado
    if produto.stock == 0:
        flash('Este produto está esgotado.', 'warning')
    
    return render_template('produtos/carros.html', produto=produto, marcas=marcas(), categorias=categorias())



@app.route('/categorias/<int:id>')
def get_categoria(id):
    pagina = request.args.get('pagina', 1, type=int)
    get_cat = Categoria.query.get_or_404(id)
    get_cat_prod = Addproduto.query.filter_by(categoria_id=get_cat.id).paginate(page=pagina, per_page=12)
    print(f"Total de produtos na categoria {get_cat.id}: {len(get_cat_prod.items)}")
    return render_template('/produtos/index.html', get_cat_prod=get_cat_prod, categorias=categorias(), marcas=marcas(), get_cat=get_cat)




# adicionar marca
@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')

# atualizar marca
@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method=='POST':
        updatemarca.name = marca
        flash(f'Sua alteração foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))

    
    return render_template('/produtos/updatemarca.html', title='Atualizar Marcas', updatemarca=updatemarca)

# DELETAR marca
@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    marca = Marca.query.get_or_404(id)   
    if request.method=='POST':
        db.session.delete (marca)
        db.session.commit()
        flash(f'A marca {marca.name} foi deletada com sucesso', 'success')
        return redirect(url_for('marcas'))
    flash(f'A marca {marca.name} não foi deletada', 'warning')
    return redirect(url_for('marcas'))

    

# adicionar categoria
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST": 
        getcat = request.form.get('categoria')
        cat = Categoria(name=getcat)
        db.session.add(cat)
        flash(f'A Categoria {getcat} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html')

# atualizar categoria
@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method=='POST':
        updatecat.name = categoria
        flash(f'Sua alteração foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))

    
    return render_template('/produtos/updatemarca.html', title='Atualizar Categoria', updatecat=updatecat)

# DELETAR categoria
@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    categoria = Categoria.query.get_or_404(id)   
    if request.method=='POST':
        db.session.delete (categoria)
        db.session.commit()
        flash(f'A categoria {categoria.name} foi deletada com sucesso', 'success')
        return redirect(url_for('categoria'))
    flash(f'A categoria {categoria.name} não foi deletada', 'warning')
    return redirect(url_for('categoria'))



# adicionar produto
@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        color = form.color.data
        tamanho = form.tamanho.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addpro = Addproduto(name=name, price=price, discount=discount, stock=stock, color=color, tamanho=tamanho, desc=desc, marca_id=marca, categoria_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'O produto {name} foi cadastrado com sucesso', 'success')
        return redirect(url_for('admin'))
        
    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form=form, marcas=marcas, categorias=categorias)

# atualizar produto
@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])
def updateproduto(id):
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)
    if request.method == "POST":
        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data
        produto.marca_id = marca
        produto.categoria_id = categoria
        produto.stock = form.stock.data
        produto.color = form.color.data
        produto.tamanho = form.tamanho.data
        produto.desc = form.discription.data

        if request.files.get('image_1'):
            if produto.image_1:  # Verifique se há uma imagem existente para excluir
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                except Exception as e:
                    print(e)
            produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            if produto.image_2:  # Verifique se há uma imagem existente para excluir
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                except Exception as e:
                    print(e)
            produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            if produto.image_3:  # Verifique se há uma imagem existente para excluir
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
                except Exception as e:
                    print(e)
            produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        db.session.commit()
        flash(f'O produto foi atualizado com sucesso', 'success')
        return redirect(url_for('admin'))

    # Preencher o formulário com os dados do produto existente
    form.name.data = produto.name   
    form.price.data = produto.price
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.color.data = produto.color
    form.tamanho.data = produto.tamanho
    form.discription.data = produto.desc

    return render_template('/produtos/updateproduto.html', title='Atualizar Produtos', form=form, marcas=marcas, categorias=categorias, produto=produto)

# DELETAR PRODUTO
@app.route('/deleteproduto/<int:id>', methods=['POST'])
def deleteproduto(id):
    if 'email' not in session:
        flash(f'Favor faça seu login primeiro', 'danger')
        return redirect(url_for('login'))
    produto = Addproduto.query.get_or_404(id)   
    try:
        os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
        os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
        os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
    except Exception as e:
        print(e)
    db.session.delete(produto)
    db.session.commit()
    flash(f'O produto {produto.name} foi deletado com sucesso', 'success')
    return redirect(url_for('admin'))



#AVALIACAO

@app.route('/avaliar_produto/<int:produto_id>', methods=['POST'])
@login_required
def avaliar_produto(produto_id):
    produto = Addproduto.query.get_or_404(produto_id)
    
    # Verificar se o cliente já comprou o produto
    pedidos = ClientePedido.query.filter_by(cliente_id=current_user.id).all()
    comprou_produto = any(str(produto_id) in pedido.pedido.keys() for pedido in pedidos)

    if not comprou_produto:
        flash('Você só pode avaliar produtos que comprou.', 'danger')
        return redirect(url_for('pagina_unica', id=produto_id))
    
    # Verificar se o cliente já avaliou o produto
    avaliacao_existente = Avaliacao.query.filter_by(cliente_id=current_user.id, produto_id=produto_id).first()
    
    if avaliacao_existente:
        flash('Você já avaliou este produto.', 'warning')
        return redirect(url_for('pagina_unica', id=produto_id))
    
    # Obter dados do formulário
    estrelas = request.form.get('estrelas')
    comentario = request.form.get('comentario')

    # Criar nova avaliação
    nova_avaliacao = Avaliacao(produto_id=produto_id, cliente_id=current_user.id, estrelas=estrelas, comentario=comentario)
    db.session.add(nova_avaliacao)
    db.session.commit()

    flash('Sua avaliação foi submetida com sucesso.', 'success')
    return redirect(url_for('pagina_unica', id=produto_id))



