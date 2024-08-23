from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_login import LoginManager
from flask_migrate import Migrate

# Definições de diretório base
basedir = os.path.abspath(os.path.dirname(__file__))

# Criação da instância do Flask
app = Flask(__name__)

# Configurações da aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhaloja.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'APP_USR-b7450fe5-74ea-46a8-a363-5e0cb0ab527a')  # Substitua pelo valor da variável de ambiente

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Inicialização do Flask-Migrate
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app)

# Inicialização do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'clientelogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Faça seu login primeiro'

# Configuração de uploads
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

# Importação de rotas
from loja.admin import rotas
from loja.produtos import rotas
from loja.carrinho import carrinhos
from loja.clientes import rotas
from loja.frete import frete_rotas

