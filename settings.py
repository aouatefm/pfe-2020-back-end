from flask import Flask
from mailjet_rest import Client

app = Flask(__name__)
DEFAULT_AVATAR_URL = "https://firebasestorage.googleapis.com/v0/b/pfe2020-fba1d.appspot.com/o/shoBig%2Fdefault-avatar.png?alt=media&token=2aa17003-2fcb-4df6-a98f-ea3ac5bf6d50"
APP_EMAIL = "no.reply.shobig@hotmail.com"
#  Mailjet keys
API_KEY = "71f114f9ae683c6d780a21709233b292"
API_SECRET = "c6c1a501d8389e6061bd6d2528285eb8"

mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')
