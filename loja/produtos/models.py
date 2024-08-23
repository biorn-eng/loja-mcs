from loja import db

from datetime import datetime


class Addproduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Text, nullable=False)
    tamanho = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'),nullable=False)
    marca = db.relationship('Marca',backref=db.backref('marca', lazy=True))

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'),nullable=False)
    categoria = db.relationship('Categoria',backref=db.backref('categoria', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addproduto %r>' % self.name



class Marca(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False, unique=True)

class Categoria(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False, unique=True)
    



class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('addproduto.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cadastrar.id'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    estrelas = db.Column(db.Integer, nullable=False)
    data_criado = db.Column(db.DateTime, default=datetime.utcnow)

    produto = db.relationship('Addproduto', backref=db.backref('avaliacoes', lazy=True))
    cliente = db.relationship('Cadastrar', backref=db.backref('avaliacoes', lazy=True))

    def __repr__(self):
        return '<Avaliacao %r>' % self.id
