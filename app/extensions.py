from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

# Singletons for all extensions
db            = SQLAlchemy()
csrf          = CSRFProtect()
migrate       = Migrate()
login_manager = LoginManager()
admin         = Admin(template_mode='bootstrap4')

