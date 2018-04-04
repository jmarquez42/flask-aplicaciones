from werkzeug import abort
from flask import Blueprint
from flask import render_template, request
from models import PRODUCTS

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/')
@product_blueprint.route('/home')
def home():
    print (request.accept_languages)
    return render_template('home.html', products=PRODUCTS)


@product_blueprint.route('/producto/<key>')
def producto(key):
    product = PRODUCTS.get(key)
    print product
    if not product:
        abort(404)
    return render_template('product.html', product=product)


@product_blueprint.context_processor
def some_processor():
    def full_name(product):
        return '{0} / {1}'.format(product['category'], product['name'])
    return {'full_name': full_name}
