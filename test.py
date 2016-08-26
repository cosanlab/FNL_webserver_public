from flask import Flask

# test whether ngingx/apache is serving flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>Am I working yet?</span>"
