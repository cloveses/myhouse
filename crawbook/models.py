import os
from pony.orm import *

db = Database()

class Book(db.Entity):
    title = Optional(str)
    writer = Optional(str)
    published = Optional(int)
    pages = Optional(int)
    downloads = Optional(int)
    tags = Optional(str)
    book_url = Required(str)

class Book_v2(db.Entity):
    title = Optional(str)
    writer = Optional(str)
    published = Optional(int)
    pages = Optional(int)
    downloads = Optional(int)
    tags = Optional(str)
    book_url = Required(str)
    visited = Required(int, default=0)

# set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)