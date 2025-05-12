from flask import Flask
from config import Config
from flask_admin.contrib.sqla import ModelView

# Import extension instances and your modelsf
from .extensions import db, csrf, migrate, login_manager, admin
from .models import User, BMI, HealthLog


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    migrate.init_app(app, db)
    login_manager.init_app(app)
    admin.init_app(app)

    # 2. Configure Flask-Login
    login_manager.login_view = 'auth_bp.login'

    # 3. Selectively exempt CSRF on non-auth routes
    from app.routes.dashboard import dashboard_bp
    from app.routes.user import user_bp
    from dashboard.admin_routes import admin_bp
    csrf.exempt(dashboard_bp)
    csrf.exempt(user_bp)
    csrf.exempt(admin_bp)

    # 4. Register blueprints (order: ensure auth_bp remains protected)
    from app.routes.auth import auth_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp)

    # 5. Add Flask-Admin views
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(BMI, db.session))
    admin.add_view(ModelView(HealthLog, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
