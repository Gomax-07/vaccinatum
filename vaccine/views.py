from flask import Flask, render_template, url_for
import requests
import json
import sys
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app._static_folder = ''
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def index():
  r = requests.get('https://corona.lmao.ninja/v2/countries/kenya')
  return render_template('index.html', stats=json.loads(r.text))

@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')




if __name__ == "__main__":
    app.run(debug=True)   
