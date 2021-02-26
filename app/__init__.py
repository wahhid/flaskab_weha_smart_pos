import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from app.index import WehaIndexView

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
#appbuilder = AppBuilder(app, db.session, base_template='adminltebase.html')
appbuilder = AppBuilder(app, db.session)

"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
from . import api

# import logging

# from flask import Flask
# from flask_appbuilder import AppBuilder, SQLA

# logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# logging.getLogger().setLevel(logging.DEBUG)

# db = SQLA()
# appbuilder = AppBuilder()

# def create_app(config):
#     app = Flask(__name__)
#     with app.app_context():
#         app.config.from_object(config)
#         db.init_app(app)
#         appbuilder.init_app(app, db.session)
#         from . import views  # noqa

#         appbuilder.post_init()
#     return app



