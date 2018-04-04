from flask import Flask
from hello.views import hello
from product.views import product_blueprint

app = Flask(__name__, template_folder='template', static_folder='static')
app.register_blueprint(hello)
app.register_blueprint(product_blueprint)


@app.template_filter('format_currency')
def format_currency_filter(amount):
    return '{0} {1}'.format("USD", amount)


