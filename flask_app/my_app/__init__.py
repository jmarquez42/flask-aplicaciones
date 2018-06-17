from flask import Flask,render_template, request,jsonify
from hello.views import hello
from product.views import product_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager


app = Flask(__name__, template_folder='template', static_folder='static')
app.register_blueprint(hello)
app.register_blueprint(product_blueprint)

#Inicia la configuracion del SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/usuario/Descargas/test1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from catalog.views import catalog
app.register_blueprint(catalog)
db.create_all()

app.secret_key = 'secret'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Filtros
@app.template_filter('format_currency')
def format_currency_filter(amount):
    return '{0} {1}'.format("USD", amount)

from functools import wraps


def template_or_json(template=None):
    """"Return a dict from your view and this will either
    pass it to a template or render json. Use like:
    @template_or_json('template.html')
    """
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_xhr or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated

