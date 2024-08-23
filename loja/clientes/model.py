from loja import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
        
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
        
@login_manager.user_loader
def user_carregar(user_id):
    return Cadastrar.query.get(user_id)

class Cadastrar(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50), unique = False)
    country = db.Column(db.String(50), unique = False)
    state = db.Column(db.String(50), unique = False)
    city = db.Column(db.String(50), unique = False)
    contact = db.Column(db.String(50), unique = False)
    address = db.Column(db.String(50), unique = False)
    zipcode = db.Column(db.String(50), unique = False)
    data_criado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Cadastrar %r>' % self.name
    
class ClientePedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notafiscal = db.Column(db.String(20), unique = True, nullable = False)
    status = db.Column(db.String(20), default = 'pendente', nullable = False)
    cliente_id = db.Column(db.Integer, unique = False, nullable = False)
    data_criado = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
    pedido = db.Column(JsonEcodedDict)
    total_pago = db.Column(db.Float, nullable=True)  # Novo campo

    def __repr__(self):
        return'<ClientePedido %r>' % self.notafiscal
