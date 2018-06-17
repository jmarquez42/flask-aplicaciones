from werkzeug import abort
from flask import Blueprint
from flask import render_template, request,jsonify
from models import PRODUCTS

product_blueprint = Blueprint('product', __name__)


@product_blueprint.route('/')
@product_blueprint.route('/home')
def home():
    if request.is_xhr:
        products = PRODUCTS.query.all()
        return jsonify({
        'count': len(products)
         })
    return render_template('home.html')

@product_blueprint.errorhandler(404)
def page_not_found(e):
    return "Pagina no ento", 404

@product_blueprint.route('/producto/<key>')
def producto(key):
    product = PRODUCTS.get(key)
    print product
    if not product:
        abort(404)
    return render_template('product.html', product=product)

# Crear formato como funciona
@product_blueprint.context_processor
def some_processor():
    def full_name(product):
        return '{0} / {1}'.format(product['category'], product['name'])
    return {'full_name': full_name}
