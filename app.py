from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Free API for currency exchange rates (No API key required)
API_URL = "https://open.er-api.com/v6/latest"

def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('rates', {})
    except requests.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return {}

@app.route('/')
def index():
    currencies = get_exchange_rates().keys()
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    amount = float(request.form.get('amount'))
    from_currency = request.form.get('from_currency')
    to_currency = request.form.get('to_currency')

    exchange_rates = get_exchange_rates()

    if not exchange_rates:
        return render_template('index.html', currencies=[], error="Unable to fetch exchange rates.")

    from_currency_rate = exchange_rates.get(from_currency)
    to_currency_rate = exchange_rates.get(to_currency)

    if from_currency_rate is None or to_currency_rate is None:
        return render_template('index.html', currencies=exchange_rates.keys(), error="Invalid currencies.")

    result = (amount / from_currency_rate) * to_currency_rate

    return render_template('index.html', currencies=exchange_rates.keys(), result=f"{result:.2f}")


if __name__ == '__main__':
    app.run(debug=True)
