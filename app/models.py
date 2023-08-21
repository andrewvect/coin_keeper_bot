from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, create_engine, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    coin_rel = db.relationship('CoinModel', cascade="all, delete", passive_deletes=True)
    subcategories_rel = db.relationship('SubCategoryModel', cascade="all, delete", passive_deletes=True)
    categories_rel = db.relationship('CategoryModel', cascade="all, delete", passive_deletes=True)
    registration_data_rel = db.relationship('RegistrationModel', cascade="all, delete", passive_deletes=True)


class Types(db.Model):
    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False, unique=False)

    subcategories_rel = db.relationship('SubCategoryModel', cascade="all, delete", passive_deletes=True)
    categories_rel = db.relationship('CategoryModel', cascade="all, delete", passive_deletes=True)


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False, unique=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    type_coin = db.Column(db.Integer, db.ForeignKey('types.id'))

    subcategory_rel = db.relationship('SubCategoryModel', backref='subcategory', passive_deletes=True)


class SubCategoryModel(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    type_coin = db.Column(db.Integer, db.ForeignKey('types.id'), default=1)

    coins_rel = db.relationship('CoinModel', cascade="all, delete", passive_deletes=True, backref='coins')


class CoinModel(db.Model):
    __tablename__ = 'coins'

    id = db.Column(db.Integer, primary_key=True)
    id_subcategory = db.Column(Integer, db.ForeignKey('subcategories.id', ondelete='CASCADE'))
    value = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, index=True, default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.user_id"))

    tags_rel = relationship('TagsModel', cascade="all, delete", passive_deletes=True, backref='tags')


class TagsModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(String(100))
    coin_id = db.Column(db.Integer, db.ForeignKey("coins.id", ondelete='CASCADE'))


class RegistrationModel(db.Model):
    __tablename__ = 'registrariton'

    id = db.Column(db.Integer, primary_key=True)
    hash_password = db.Column(db.String(128))
    username = db.Column(db.VARCHAR, nullable=False, unique=False)
    telegram_user = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))


engine = create_engine(SQLALCHEMY_DATABASE_URI)
db.metadata.create_all(engine)
