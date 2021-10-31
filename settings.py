from flask import Flask
from mailjet_rest import Client

app = Flask(__name__)
DEFAULT_AVATAR_URL = "https://png.pngtree.com/png-clipart/20200701/original/pngtree-character-default-avatar-png-image_5407167.jpg"
APP_EMAIL = "no.reply.shobig@hotmail.com"
#  Mailjet keys
API_KEY = "71f114f9ae683c6d780a21709233b292"
API_SECRET = "c6c1a501d8389e6061bd6d2528285eb8"

mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')
