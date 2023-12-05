from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.fda.gov/food/enforcement.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form.get('input')
    params = {'search': user_input}

    # Make API request
    response = requests.get(API_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        recalls = data.get('results', [])
        return render_template('results.html', recalls=recalls, user_input=user_input)
    else:
        return f"<h1>No items were found! <h1>"


if __name__ == '__main__':
    app.run(debug=True)

    #comment