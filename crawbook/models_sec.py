import os
from pony.orm import *

db = Database()

class Book(db.Entity):
    title = Required(str)
    writer = Required(str)
    release_date = Required(str)
    downloads = Required(str)
    tags = Required(str)
    book_url = Required(str)

class Visited(db.Entity):
    url = Required(str)

# set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my_sec.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)