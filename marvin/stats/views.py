
from flask import Flask
from flask import render_template
from marvin.client import connect


def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

app = Flask(__name__, static_url_path='/static')
app.jinja_env.filters['sizeof_fmt'] = sizeof_fmt



@app.route('/')
def home_page():
    # get list of transfered files
    server = connect()
    hist_files = server.hist()
    current_files = server.list_sending()
    return render_template('home_page.html',
                           hist_files=hist_files,
                           current_files=current_files)

def start():
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)

if __name__ == "__main__":
    start()