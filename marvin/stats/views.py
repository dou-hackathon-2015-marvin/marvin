
from flask import Flask
from flask import render_template
import logging

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home_page():

    return render_template('home_page.html', name=None)

if __name__ == '__main__':
    app.run(debug=True)