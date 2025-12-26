from flask import Flask
from flask_cors import CORS
from backend.config import config
from backend.routes.auth import auth_bp
from backend.routes.admin import admin_bp
from backend.routes.customer import customer_bp
from backend.routes.shared import shared_bp

app = Flask(__name__)
app.config.from_object(config)

# Enable CORS
CORS(app, origins=config.CORS_ORIGINS)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(customer_bp, url_prefix='/api/customer')
app.register_blueprint(shared_bp, url_prefix='/api/shared')

@app.route('/')
def index():
    return {'message': 'Online Bookstore API'}

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
