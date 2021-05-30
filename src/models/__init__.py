from flask_sqlalchemy import SQLAlchemy
from flask_bycrypt import Bcrypt

# initialize db
db = SQLAlchemy()

bcrypt = Bcrypt()