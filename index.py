from flask import Flask, render_template, request, g, redirect 
import sqlite3
import requests
import math

app = Flask(__name__)
database = 'datafile.db'

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(database)
    return g.sqlite_db

@app.teardown_appcontext
def close_connection(exception):
    # print("我們正在關閉sql connection...")
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    

@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    result = cursor.execute("select * from cash")
    cash_result = result.fetchall()
    #計算台幣與美金的總額
    taiwanese_dollars = 0
    us_dollars = 0
    for data in cash_result:
        taiwanese_dollars += data[1]
        us_dollars += data[2]
    
    #獲取匯率資訊
    r = requests.get('https://tw.rter.info/capi.php')
    currency=r.json()   
    total = math.floor(taiwanese_dollars + us_dollars * currency['USDTWD']['Exrate'])
    
    data = {'total': total, 'currency': currency['USDTWD']['Exrate'], 'ud':us_dollars, 'td':taiwanese_dollars, 'cash_result': cash_result}
    
    return render_template('index.html', data = data)

@app.route('/cash')
def cash_form():
    return render_template('cash.html')

@app.route('/cash', methods=['POST'])
def submit_cash():
    
    #取得金額日期資料
    taiwanese_dollars = 0
    us_dollars = 0
    if request.values['taiwanese-dollars']!= '':
        taiwanese_dollars = request.values['taiwanese-dollars']
    if request.values['us-dollars']!= '':
        us_dollars = request.values['us-dollars']
    note = request.values['note']
    date = request.values['date']
    
    #Update Database information
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""insert into cash (taiwanese_dollars, us_dollars, note, date_info) values(?,?,?,?)""", (taiwanese_dollars, us_dollars, note, date))
    
    conn.commit()
    
    #redirect users back to homepage
    return redirect("/")
    
    
    return "感謝提交表單"

@app.route('/stock')
def stock_form():
    return render_template('stock.html')

if __name__ == '__main__':
    app.run(debug=True)