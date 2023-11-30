from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests, json


app = Flask(__name__)
bootstrap = Bootstrap5(app)

# api_date_string = recall_initiation_date

# api_date = datetime.strptime(api_date_string, "%Y-%m-%dT%H:%M:%S")


API_URL = "https://api.fda.gov/food/enforcement.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    user_input = request.form.get('input')
    params = {'search': user_input}
    
    response = requests.get(API_URL, params = params)

    try:
        data = response.json()
        recalls = data.get('results', [])
        return render_template('results.html', recalls = recalls, user_input = user_input)
    except:
        return render_template('results.html', no_results = True, user_input = user_input)