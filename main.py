from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests, json


app = Flask(__name__)
bootstrap = Bootstrap5(app)




API_URL = "https://api.fda.gov/food/enforcement.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    user_input = request.form.get('input')
    params = {'search': user_input}
    
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
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
            
            
                
            return render_template('results.html', recalls = recalls, user_input = user_input, recallDate = recallDate, reportDate = reportDate)
       except:
            pass
    else:
        return render_template('results.html', no_results = True, user_input = user_input)