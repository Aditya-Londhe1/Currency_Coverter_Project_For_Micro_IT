from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    chart_data = {}

    # Get currency list
    res = requests.get("https://api.frankfurter.app/currencies")
    currencies = sorted(res.json().keys())

    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_curr = request.form['from_currency']
        to_curr = request.form['to_currency']

        if from_curr != to_curr:
            url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_curr}&to={to_curr}"
            response = requests.get(url).json()
            result = round(response['rates'][to_curr], 2)

            # Optional: last 7 days chart
            chart_url = f"https://api.frankfurter.app/2024-05-30..2024-06-05?from={from_curr}&to={to_curr}"
            chart_res = requests.get(chart_url).json()
            chart_data = {
                "dates": list(chart_res['rates'].keys()),
                "rates": [v[to_curr] for v in chart_res['rates'].values()]
            }

    return render_template('index.html', currencies=currencies, result=result, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
