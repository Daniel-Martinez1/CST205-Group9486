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
    page = int(request.args.get('page', 1))
    per_page = 10
    params = {'search': user_input, 'limit': per_page, 'skip': (page - 1) * per_page}

    response = requests.get(API_URL, params = params)

    try:
        data = response.json()
        recalls = data.get('results', [])
        for recall in recalls:
           datestr = recall['report_date']
           year = datestr[0:4]  
           month = datestr[5:6]
           day = datestr[6:8]
        reportDate = f"{month}/{day}/{year}"
        for recall in recalls:
           datestr = recall['recall_initiation_date']
           year = datestr[0:4]
           month = datestr[5:6]
           day = datestr[6:8]
        recallDate = f"{month}/{day}/{year}"
        print(recall)
        return render_template('results.html', recalls = recalls, user_input = user_input, recallDate =  recallDate, reportDate = reportDate, page=page)
    except:
        return render_template('results.html', no_results = True, user_input = user_input)