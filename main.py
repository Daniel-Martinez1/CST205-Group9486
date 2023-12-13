from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests, json

app = Flask(__name__)
bootstrap = Bootstrap5(app)

API_URL = "https://api.fda.gov/food/enforcement.json"

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('home.html')

# Daniel Martinez Start
@app.route('/search', methods = ['POST'])
def search():
    state = request.form.get('state')
    city = request.form.get('city')
    recall_item = request.form.get('recall')
    user_input = str(state) + str(city) + str(recall_item)
    params = {'search':input, 'limit': 20, 'skip': 0}
    user_input = f'{state} {city} {recall_item}'
    response = requests.get(API_URL, params = params)

    try:
        data = response.json()
        recalls = data.get('results', [])
        for recall in recalls:
           datestr = recall['report_date']
           year = datestr[0:4]
           month = datestr[4:6]
           day = datestr[6:8]
           reportDate = f"{month}/{day}/{year}"
           recall['report_date'] = reportDate
        for recall in recalls:
           datestr = recall['recall_initiation_date']
           year = datestr[0:4]
           month = datestr[4:6]
           day = datestr[6:8]
           recallDate = f"{month}/{day}/{year}"
           recall['recall_initiation_date'] = recallDate
        print(recalls)
        return render_template('results.html', recalls = recalls, user_input = user_input, recallDate =  recallDate, reportDate = reportDate)
    except:
        return render_template('results.html', no_results = True, user_input = user_input)
# Daniel Martinez End
