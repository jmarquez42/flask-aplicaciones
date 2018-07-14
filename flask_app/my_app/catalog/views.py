from flask import request, jsonify, Blueprint, render_template,render_template_string,flash,redirect,url_for
from flask_app.my_app import db,app
from flask_app.my_app.catalog.models import Product, Category, ProductForm
from flask.views import MethodView
from werkzeug.utils import secure_filename
from flask_app.my_app import ALLOWED_EXTENSIONS
import os


def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home2')

def home():
    if request.is_xhr:
        products = Product.query.all()
        return jsonify({
        'count': len(products)
         })
    return render_template('home.html')


@catalog.route('/a-get-request')
def get_request():
    bar= request.args.get('foo','get')
    template = str('''<html><head></head><h2>Hello %s!</h2></html>''') % bar
    return render_template(template,bar=bar)


@catalog.route('/a-post-request', methods=['POST'])
def post_request():
    bar = request.args.get('foo', 'post')
    return 'A simple Flask request where foo is %s' % bar


@catalog.route('/a-request', methods=['POST', 'GET'])
def same_request():
    if request.method == 'GET':
        bar = request.args.get('foo', 'get')
    else:
        bar = request.args.get('foo', 'post')
    return 'A simple Flask request where foo is %s' % bar


@catalog.route('/products')
@catalog.route('/products/page')
def products(page=1):
    #products = Product.query.all()
    products = Product.query.paginate(page,3)
    #print products.items
    print page
    return render_template('products.html', products=products)
   # res={}
   #  for product in products:
   #      res[product.id] = {
   #          'name': product.name,
   #          'price': str(product.price),
   #          'category': product.category.name,
   #          'company':product.company
   #      }
   #  return jsonify(res)




@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    #return 'Product - %s,$%s' %(product.name, product.price)
    return render_template('product.html',product=product)

@catalog.route('/product-create', methods=['POST','GET'])
def create_product():
    form = ProductForm(request.form, csrf_enabled=False)
    categories = [(c.id, c.name) for c in Category.query.all()]

    form.category.choices = categories
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = Category.query.get_or_404(request.form.get('category'))
        company = request.form.get('company')

        product = Product(name=name, price=price,category=category,company=company)
        db.session.add(product)
        db.session.commit()
        flash('The product %s has been created' % name, 'info')
        return redirect(url_for('catalog.product', id=product.id))
    return render_template('product-create.html',form=form)

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





class GetPostRequest(MethodView):

    def get (self):
        bar = request.args.get('foo', 'get')
        return 'Class a simple Flask request where foo is %s' % bar

    def post (self):
        bar = request.args.get('foo', 'post')
        return 'Class a simple Flask request where foo is %s' % bar

catalog.add_url_rule('/a-request-class', view_func=GetPostRequest.as_view('a-request-class'))


@catalog.route('/catalog/test/<string(minlength=2,maxlength=3):code>')
def get_name(code):
    return code

@catalog.route('/catalog/test/<int:age>')
def get_age(age):
    return str(age)

@catalog.route('/catalog/test/<path:file>')
def get_file(file):
    return file

