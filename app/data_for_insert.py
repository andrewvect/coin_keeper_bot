from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import importlib.util
import os

current_path = os.getcwd() + '/app/config.py'

# Specify the path to the module file
module_path = current_path

# Load the module from the specified path
spec = importlib.util.spec_from_file_location('module', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Now you can access the variable from the imported module
sql_uri = module.SQLALCHEMY_DATABASE_URI


def insert_data():
    try:
        engine = create_engine(sql_uri)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = """INSERT INTO types (name) VALUES ('expenses'), ('incomes');"""
        session.execute(query)
        session.commit()

        session.close()
    except Exception as e:
        print(e)


def check_data():

    engine = create_engine(sql_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = """SELECT COUNT(*) FROM types;"""

    data = session.execute(query)
    session.commit()
    session.close()

    count = 0

    for i in data:
        count += i[0]

    if count == 2:
        print('db already set')
    else:
        insert_data()
        print('add application data to db')


if __name__ == "__main__":
    check_data()


