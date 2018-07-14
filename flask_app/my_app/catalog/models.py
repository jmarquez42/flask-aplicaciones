from flask_app.my_app import db
from flask_wtf import Form
from wtforms import TextField, DecimalField, SelectField, FileField


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))

    # Variable que realiza el join
    category = db.relationship(
        'Category',backref=db.backref('products',lazy='dynamic')
    )
    company = db.Column(db.String(100))
    marca = db.Column(db.String(50))
    image = db.Column(db.String(255))

    def __init__(self, name, price ,category,company, image_path):
        self.name = name
        self.price = price
        self.category = category
        self.company = company
        self.image_path = image_path

    def __repr__(self):
        return '<Product %d>' % self.id

class ProductForm(Form):
    name = TextField('Name')
    price = DecimalField('Price')
    category = SelectField('Category', coerce=int)

class ProductForm(NameForm):
    image = FileField('Product Image')



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %d>' % self.id