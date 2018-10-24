from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
import datetime
app = Flask(__name__)
app.secret_key = 'mySecret'
@app.route('/')
def index():
    mysql = connectToMySQL("lead_gen_business")
    now = datetime.datetime.now()
    if 'start_date' in session:
        session['start_date'] = session['start_date']
    else:
        session['start_date'] = "1900-01-01"
    if 'end_date' in session:
        session['end_date'] = session['end_date']
    else:
        session['end_date'] = now.strftime("%Y-%m-%d")
    
    query = "SELECT clients.client_id, clients.first_name, clients.last_name, COUNT(leads.leads_id) AS leads, DATE(leads.registered_datetime) AS registered_date FROM clients JOIN sites on sites.client_id = clients.client_id JOIN leads on leads.site_id = sites.site_id WHERE leads.registered_datetime >= %(start_date)s AND leads.registered_datetime <= %(end_date)s GROUP BY clients.client_id ORDER BY leads DESC"
    data = {
        'start_date': session['start_date'],
        'end_date': session['end_date']
    }
    all_leads = mysql.query_db(query, data)
    return render_template('index.html', lead_data = all_leads)

@app.route('/set_date', methods=['POST'])
def set_date():
    session['start_date'] = datetime.datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    session['end_date'] = datetime.datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)