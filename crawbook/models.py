import os
from pony.orm import *

db = Database()

class Book(db.Entity):
    title = Required(str)
    writer = Required(str)
    published = Required(int)
    pages = Required(int)
    downloads = Required(int)
    tags = Required(str)

# set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)