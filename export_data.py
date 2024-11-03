import os
from pyairtable import Api

AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
AIRTABLE_KEY = os.environ['AIRTABLE_KEY']
AIRTABLE_TABLES = os.environ['AIRTABLE_TABLES']

api = Api(AIRTABLE_KEY)
table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLES)
table.all()