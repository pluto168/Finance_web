from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cash')
def cash_form():
    return render_template('cash.html')

@app.route('/stock')
def stock_form():
    return render_template('stock.html')

if __name__ == '__main__':
    app.run(debug=True)