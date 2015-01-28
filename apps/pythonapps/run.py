#!/usr/bin/env python
import os
from flask import Flask, jsonify
import requests
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, String, MetaData, create_engine

app = Flask(__name__)


# see http://landregistry.data.gov.uk/app/hpi/qonsole
PPI_QUERY_TMPL = """
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix lrppi: <http://landregistry.data.gov.uk/def/ppi/>
prefix lrcommon: <http://landregistry.data.gov.uk/def/common/>

# Returns the Price Paid data from the default graph for each transaction record having
# an address with the given postcode.
# The postcode to query is set in the line - ?address_instance common:postcode "PL6 8RU"^^xsd:string .


SELECT ?paon ?saon ?street ?town ?county ?postcode ?amount ?date ?property_type
WHERE
{{
    ?transx lrppi:pricePaid ?amount ;
            lrppi:transactionDate ?date ;
            lrppi:propertyAddress ?addr ;
            lrppi:propertyType ?property_type.

{}
    ?addr lrcommon:postcode ?postcode.

    OPTIONAL {{?addr lrcommon:county ?county}}
    OPTIONAL {{?addr lrcommon:paon ?paon}}
    OPTIONAL {{?addr lrcommon:saon ?saon}}
    OPTIONAL {{?addr lrcommon:street ?street}}
    OPTIONAL {{?addr lrcommon:town ?town}}

}}
ORDER BY ?amount
"""


def get_property_type(url):
    return url.partition('http://landregistry.data.gov.uk/def/common/')[2]


def get_query_parts(query_dict):
    query_tmpl = '  ?addr lrcommon:{} "{}"^^xsd:string.'
    query_lines = [query_tmpl.format(k, v) for k, v in query_dict.items()]
    return '\n'.join(query_lines)


@app.route('/properties/<postcode>/<street_paon_saon>', methods=['GET'])
def get_tasks(postcode, street_paon_saon):
    parts = street_paon_saon.upper().split('_')
    if len(parts) not in [2, 3]:
        raise ValueError('Could not split combined street, PAON and SAON into '
                         'respective parts. Expected street_PAON_SAON.')

    query_dict = {
        'postcode': postcode.upper(),
        'street': parts[0],
        'paon': parts[1],
    }
    if len(parts) == 3:
        query_dict['saon'] = parts[2]

    query = PPI_QUERY_TMPL.format(get_query_parts(query_dict))
    ppi_url = 'http://landregistry.data.gov.uk/landregistry/query'
    resp = requests.post(ppi_url, data={'output': 'json', 'query': query})

    sale_list = resp.json()['results']['bindings']

    latest_sale_date = ''
    latest_sale = None
    for sale in sale_list:
        sale_date = sale['date']['value']
        latest_sale_date = max(sale_date, latest_sale_date)
        if latest_sale_date == sale_date:
            latest_sale = sale

    result = {
        'saon': 'saon goes here',
        'paon': 'paon goes here',
        'street': 'street goes here',
        'town': 'town goes here',
        'county': 'county goes here',
        'postcode': 'postcode goes here',
        'amount': latest_sale['amount']['value'],
        'date': latest_sale['date']['value'],
        'property_type':
            get_property_type(latest_sale['property_type']['value']),
        'coordinates' : {'latitude': 99, 'longitude': 99},
    }

    return jsonify(result)

@app.route('/')
def read_from_db():
    #import pdb;pdb.set_trace()
    metadata = MetaData()

    # Reflecting the DB structure - in this case it's the 'property' table
    # Here's more about defining tables: http://docs.sqlalchemy.org/en/rel_0_9/core/tutorial.html#define-and-create-tables
    property_table = Table('public_address', metadata, Column('title_no', String), Column('uprn', String))

    # Connecting to lr_test database
    engine = create_engine('postgresql+pg8000://postgres_user:password@localhost:5432/my_postgres_db', echo=True)
    connection = engine.connect()

    try:
        # Preparing the select query - in this case it's just a simple select, with no joins, no filters.
        # You can find more information about selecting here: http://docs.sqlalchemy.org/en/rel_0_9/core/tutorial.html#selecting
        query = select([property_table.c.title_no, property_table.c.uprn]).where(property_table.c.title_no == 'DT100')

        # A function that converts a single result row into a string - we'll use it to convert the whole query result into a string
        def result_row_to_string(row):
            return 'title: "{}", uprn: "{}"'.format(row[property_table.c.title_no], row[property_table.c.uprn])

        query_result = connection.execute(query)

        # Preparing results - all the retrieved rows converted to strings and joined using new line character
        result_string = '\n'.join(map(result_row_to_string, query_result.fetchall()))
        if not result_string:
            result_string = "Details not found"
        return result_string
    finally:
        query_result.close()
        connection.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
