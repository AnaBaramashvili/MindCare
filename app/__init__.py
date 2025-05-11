from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context(): 
        from app.models import User, BMI, HealthLog
        db.create_all()

        
        admin = Admin(app, name='MindCare Admin', template_mode='bootstrap4')
        admin.add_view(ModelView(User, db.session))
        admin.add_view(ModelView(BMI, db.session))
        admin.add_view(ModelView(HealthLog, db.session))

        
        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.user import user_bp
        from dashboard.admin_routes import admin_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')


    return app
