from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, PasswordField, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from.model import Cadastrar
from wtforms.validators import ValidationError, DataRequired, Length


class CadastroClienteForm(FlaskForm):
    name = StringField ('Nome:')
    username = StringField ('Usuario:', [validators.DataRequired()])
    email = StringField ('Email:', [validators.DataRequired()])
    password = PasswordField ('Senha:', [validators.DataRequired(), validators.EqualTo('confirm', message='As duas senhas devem ser iguais')])
    confirm = PasswordField ('Redigite Senha:', [validators.DataRequired()])
    country = StringField ('País:', [validators.DataRequired()])
    state = StringField ('Estado:', [validators.DataRequired()])
    city = StringField ('Cidade:', [validators.DataRequired()])
    contact = StringField ('Contato:', [validators.DataRequired()])
    address = StringField ('Endereço:', [validators.DataRequired()])
    zipcode = StringField ('CEP:', [validators.DataRequired()])

    submit = SubmitField ('Cadastrar')

    def validate_username(self, username):
        if Cadastrar.query.filter_by(username=username.data).first():
            raise ValidationError ("Este usuario já existe")
        
    def validate_email(self, email):
        if Cadastrar.query.filter_by(email=email.data).first():
            raise ValidationError ("Este email já existe")
        

class ClienteLoginForm(FlaskForm):
    email = StringField ('Email:', [validators.DataRequired()])
    password = PasswordField ('Senha:', [validators.DataRequired()])


class AtualizaClienteForm(FlaskForm):
    name = StringField('Nome:', [DataRequired(), Length(max=50)])
    username = StringField('Usuario:', [DataRequired(), Length(max=50)])
    email = StringField('Email:', [DataRequired(), Length(max=50)])
    country = StringField('País:', [DataRequired(), Length(max=50)])
    state = StringField('Estado:', [DataRequired(), Length(max=50)])
    city = StringField('Cidade:', [DataRequired(), Length(max=50)])
    contact = StringField('Contato:', [DataRequired(), Length(max=50)])
    address = StringField('Endereço:', [DataRequired(), Length(max=50)])
    zipcode = StringField('CEP:', [DataRequired(), Length(max=20)])
    submit = SubmitField('Atualizar')