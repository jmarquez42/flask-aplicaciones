from flask import Flask
from hello.views import hello
from product.views import product_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,Manager,MigrateCommand

app = Flask(__name__, template_folder='template', static_folder='static')
app.register_blueprint(hello)
app.register_blueprint(product_blueprint)

#Inicia la configuracion del SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from catalog.views import catalog
app.register_blueprint(catalog)
db.create_all()


#Filtros
@app.template_filter('format_currency')
def format_currency_filter(amount):
    return '{0} {1}'.format("USD", amount)


