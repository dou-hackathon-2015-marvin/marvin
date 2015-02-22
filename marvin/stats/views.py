import json
from datetime import datetime

from flask import Flask
from flask import render_template
from marvin.client import connect


def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

def format_dt(tms):
    return datetime.fromtimestamp(tms)


app = Flask(__name__, static_url_path='/static')
app.jinja_env.filters['sizeof_fmt'] = sizeof_fmt
app.jinja_env.filters['datetime'] = format_dt
server = connect()


def get_stats(templ):
    hist_files = server.hist()
    hist_files.sort(key=lambda x: x.start_time, reverse=True)
    current_files = server.list_sending()
    return render_template(templ,
                           hist_files=hist_files,
                           current_files=current_files)

@app.route('/')
def home_page():
    return get_stats('home_page.html')

@app.route("/stats")
def stats():
    return get_stats('stats.html')

def start():
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)

if __name__ == "__main__":
    start()