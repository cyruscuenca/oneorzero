from pymongo import MongoClient
from functools import reduce
from pymemcache.client.base import Client

memcache = Client('localhost')
client = MongoClient()
db = client['oneorzero']

def recache():

    print('reaching')
    #try:

    # Read component keys from a config file
    tables = open('../../config/component_table_keys', 'r').read()
    tables = tables.splitlines(True)

    # Cache all the possible keys in files on disk
    for table in tables:

        table = table.strip('\n')

        # Find all unique keys
        keys = reduce(
            lambda all_keys, rec_keys: all_keys | set(rec_keys), 
            map(lambda d: d.keys(), db[table].find()), 
            set()
        )

        memcache.set(table.lower() + str('_keys'), list(keys))

    #except:

        #return False
        
    return True