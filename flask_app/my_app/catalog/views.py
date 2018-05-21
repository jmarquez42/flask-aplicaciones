from flask import request, jsonify, Blueprint
from flask_app.my_app import db,app
from flask_app.my_app.catalog.models import Product, Category

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home2')
def home():
    return "Welcome to the Catalog Home."


@catalog.route('/products')
def products():
    products = Product.query.all()
    res={}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': str(product.price),
            'category': product.category.name
        }
    return jsonify(res)


@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return 'Product - %s,$%s' %(product.name, product.price)


@catalog.route('/product-create', methods=['POST',])
def create_product():
    name = request.form.get('name')
    price = request.form.get('price')
    categ_name = request.form.get('category')
    category = Category.query.filter_by(name = categ_name).first()
    if not category:
        category=Category(categ_name)
    product = Product(name=name, price=price, category=category)
    db.session.add(product)
    db.session.commit()
    return 'Product create.'

@catalog.route('/category-create', methods=['POST',])
def create_category():
    name = request.form.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return 'Category created.'

@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    res = {}
    for category in categories:
        res[category.id] = {
            'name': category.name
        }
        for product in category.products:
            res[category.id]['products'] = {
                'id': product.id,
                'name': product.name,
                'price': product.price
    }
    return jsonify(res)


