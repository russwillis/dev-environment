#!/usr/bin/python

# In order to be able to execute this script, you need to install sqlalchemy: 'pip install SQLAlchemy'
# The script assumes, that you've got:
# - a local instance of postgresql, listening on the default port (5432)
# - database called lr_test, with 'property' table, containing 'title' and 'uprn' columns

from flask import Flask
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, String, MetaData, create_engine

app = Flask(__name__)

# This endpoint executes a simple select query against the test database (lr_test) and returns the result.
# In order to call it, just run 'curl http://127.0.0.1:5000' (or whatever port the service is listening on)
@app.route('/')
def read_from_db():
    #import pdb;pdb.set_trace()
    metadata = MetaData()

    # Reflecting the DB structure - in this case it's the 'property' table
    # Here's more about defining tables: http://docs.sqlalchemy.org/en/rel_0_9/core/tutorial.html#define-and-create-tables
    property_table = Table('property', metadata, Column('title', String), Column('uprn', String))

    # Connecting to lr_test databse
    engine = create_engine('postgresql://localhost:5432/lr_test', echo=True)
    connection = engine.connect()

    try:
        # Preparing the select query - in this case it's just a simple select, with no joins, no filters.
        # You can find more information about selecting here: http://docs.sqlalchemy.org/en/rel_0_9/core/tutorial.html#selecting
        query = select([property_table.c.title, property_table.c.uprn])

        # A function that converts a single result row into a string - we'll use it to convert the whole query result into a string
        def result_row_to_string(row): return 'title: "{}", uprn: "{}"'.format(row[property_table.c.title], row[property_table.c.uprn]) 

        query_result = connection.execute(query)

        # Preparing results - all the retrieved rows converted to strings and joined using new line character
        result_string = '\n'.join(map(result_row_to_string, query_result.fetchall())) 
        return result_string
    finally:
        query_result.close()
        connection.close()    

if __name__ == '__main__':
    app.run()

