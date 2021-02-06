from flask import Flask
from apis import *
import apis
from settings import app


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
