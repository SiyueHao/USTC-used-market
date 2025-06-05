from flask import Flask
from api.user_api import user_bp
from api.product_api import product_bp
app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(product_bp, url_prefix='/product')

if __name__ == '__main__':
    app.run(debug=True)
