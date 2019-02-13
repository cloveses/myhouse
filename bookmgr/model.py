import os
from pony.orm import *

db = Database()

class UserDb(db.Entity):
    username = Required(str)
    password = Required(str)

class BookDb(db.Entity):
    bookname = Required(str)
    author = Required(str)
    category = Required(str)
    price = Required(str)
    desc = Required(str)
    publish_date = Required(str)

# set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)