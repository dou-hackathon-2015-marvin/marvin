
from flask import Flask
from flask import render_template
from marvin import client
import logging

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home_page():
    # get list of transfered files
    files = client.list_files()
    return render_template('home_page.html', files=files)

def start():
    app.run(debug=True)
