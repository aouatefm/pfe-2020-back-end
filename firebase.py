import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client

cred = credentials.Certificate("./credentials/pfe2020-firebase.json")
firebase_admin.initialize_app(cred)
fs: Client = firestore.client()

COLLECTIONS = dict(users='users',
                   stores='stores',
                   products='products',
                   categories='categories',
                   ratings='ratings',
                   orders='orders',
                   coupons='coupons',
                   )
