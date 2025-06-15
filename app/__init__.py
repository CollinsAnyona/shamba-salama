from flask import Flask
from app.services.initial_data import create_default_data
from app.config import Config
from app.extensions import db, login_manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(name='Admin Panel', template_mode='bootstrap4')


def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    
    from .users import users_bp, auth_bp
    from .products import products_bp
    from .bookings import bookings_bp
    from .posts import posts_bp
    from .main import main_bp
    from .shambabot import shambabot_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(shambabot_bp)
    
    admin.init_app(app)
    # Register models with Flask-Admin
    from app.users.models import User
    from app.products.models import Product
    from app.bookings.models import Booking
    from app.posts.models import Post
    
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Booking, db.session))
    admin.add_view(ModelView(Post, db.session))
    
    

    @app.after_request
    def add_header(response):
        response.cache_control.no_cache = True
        return response

    # Initialize database and default data
    with app.app_context():
        db.create_all()
        create_default_data()

    return app
