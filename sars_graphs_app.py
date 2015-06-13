from datetime import datetime
from dateutil.parser import parse

import os

from flask import Flask
from flask import render_template

import filenames

app = Flask(__name__)


@app.route('/')
@app.route("/hello", methods=['GET'])
def show_stats():
    with open(filenames.SARS_QUEUE_STATS) as f:
        #  reverse file for most recent dates at end of file first
        raw = f.read().strip().split("\n")
        raw = raw[-300:]
        data = []
        for line in raw:
            s_date, people = line.split(", ")
            date = datetime.strftime(parse(s_date), '%d %B @ %H:%M')
            data.append({'date': date, 'people': int(people)})
        return render_template("queues.html", data=data)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

