from flask import Flask
from flask_cors import CORS
from config import Config
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.customer import customer_bp
from routes.shared import shared_bp

def create_app(config_class=Config):
    # Point to frontend directory
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.config.from_object(config_class)
    
    # Enable CORS if frontend is separate (likely)
    CORS(app, supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(customer_bp, url_prefix='/customer') # customer routes usually under /customer or root?
    # File structure notes: /customer/dashboard.html, routes/customer.py etc.
    # routes/customer.py endpoints: /cart/add, /cart etc.
    # If I prefix with /customer, then it is /customer/cart.
    # The file structure says "POST /cart/add" in routes/customer.py description.
    # This implies root level or maybe just implicit.
    # However, to avoid conflicts, let's look at `routes/customer.py` content I wrote.
    # I wrote `@customer_bp.route('/cart', ...)`
    # If I register without prefix, it's `/cart`. If with, `/customer/cart`.
    # `auth.py` has /login.
    # `admin.py` has /admin/books (I set url_prefix='/admin' inside admin.py).
    # `customer.py` methods seem to be mostly unique (/cart, /checkout, /orders, /profile).
    # So I will register customer_bp without prefix or maybe API prefix.
    # Let's register without prefix for now as the names are quite distinct.
    
    # Re-registering to fix prefix if needed.
    # `shared` has /books/search which might conflict if admin has /books? 
    # Admin has /admin/books. Shared has /books. Safe.
    
    app.register_blueprint(shared_bp)
    
    # Note: customer_bp defined in my code above didn't have url_prefix.
    # I will register it at root level for now.
    app.register_blueprint(customer_bp)

    from flask import render_template
    
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
