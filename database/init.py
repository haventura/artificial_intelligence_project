import sqlalchemy

url = 'mysql://username:password@14.41.50.12/dbname'

engine = create_engine(url, echo=True)
connection = engine.connect()

sqlalchemy.ext.declarative.declarative_base