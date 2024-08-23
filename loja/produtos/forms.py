from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField


class Addprodutos(Form):
    name = StringField('Nome:', [validators.DataRequired()])
    price = DecimalField('Preço:', [validators.DataRequired()])
    discount = IntegerField('Desconto:', [validators.DataRequired()])
    stock = IntegerField('Estoque:', [validators.DataRequired()])
    discription = TextAreaField('Descrição:', [validators.DataRequired()])
    color = TextAreaField('Cor:', [validators.DataRequired()])
    tamanho = TextAreaField('Tamanho:', [validators.DataRequired()])

    image_1 = FileField('Image_1:' , validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Image_2:' , validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image_3:' , validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

