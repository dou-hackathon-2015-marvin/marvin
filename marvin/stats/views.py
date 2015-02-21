
from flask import Flask
from flask import render_template
from marvin import client
app = Flask(__name__)

@app.route('/')
def home_page():
    # get list of transfered files
    files = client.list_files()
    return render_template('home_page.html', files=files)

def start():
    app.run(debug=True)
