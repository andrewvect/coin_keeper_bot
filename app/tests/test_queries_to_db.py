import datetime
import unittest
from app.app import app
from coin_bot.Coin_bot.app.queries_to_db import is_user_in_database, add_user_to_database, add_category_to_user
from coin_bot.Coin_bot.app.models import db, UserModel, CategoryModel
from coin_bot.Coin_bot.app.config import SQLALCHEMY_DATABASE_URI_FOR_TESTS


class TestIsUserInDatabase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_FOR_TESTS
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_not_in_database(self):
        with app.app_context():
            user = UserModel(user_id='123')
            db.session.add(user)
            db.session.commit()

        exists = is_user_in_database('456', app.app_context())
        self.assertFalse(exists)

    def test_user_in_database(self):
        with app.app_context():
            user = UserModel(user_id='123')
            db.session.add(user)
            db.session.commit()

        exists = is_user_in_database('123', app.app_context())
        self.assertTrue(exists)


class TestAddUserToDatabase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_FOR_TESTS
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user_to_database(self):
        with app.app_context():
            add_user_to_database(123, app.app_context())

            user = UserModel.query.filter_by(user_id=123).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.user_id, 123)
            self.assertIsInstance(user.created_at, datetime.datetime)


class TestAddCategoryToUser(unittest.TestCase):
    def setUp(self):
        # Set up a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_FOR_TESTS
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Remove the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_category_to_user(self):
        # Add a user to the database
        with app.app_context():
            user = UserModel(user_id=123)
            db.session.add(user)
            db.session.commit()

            # Add a spending category to the user
            add_category_to_user(123, 'Groceries', 'spending', app.app_context())

            # Check if the category was added successfully
            category = CategoryModel.query.filter_by(name='Groceries').first()
            self.assertIsNotNone(category)
            self.assertEqual(category.name, 'Groceries')
            self.assertEqual(category.user_id, 123)
            self.assertEqual(category.type_coin, 1)

            # Add an incomes category to the user
            add_category_to_user(123, 'Salary', 'incomes', app.app_context())

            # Check if the category was added successfully
            category = CategoryModel.query.filter_by(name='Salary').first()
            self.assertIsNotNone(category)
            self.assertEqual(category.name, 'Salary')
            self.assertEqual(category.user_id, 123)
            self.assertEqual(category.type_coin, 2)


if __name__ == '__main__':
    unittest.main()
