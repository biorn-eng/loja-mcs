from flask import Flask
from loja import app, db, migrate

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados
        migrate.init_app(app, db)  # Inicializa as migrações
    app.run(debug=True)
