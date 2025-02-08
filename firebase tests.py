import firebase_admin as fba
from assets.gamelib.const import *
from firebase_admin import db


cred = fba.credentials.Certificate(DBCERT)
key = 'test1'
data = 'hii'

default_app = fba.initialize_app(cred, {
    "databaseURL": DBURL
    })
ref = db.reference(f"/{key}/")
ref.set(data)
ref = db.reference('/test/')
print(ref.get())