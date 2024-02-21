import csv
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# SQLite3 Database Setup
conn = sqlite3.connect('app/dataset.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS clients 
             (id INTEGER PRIMARY KEY, category TEXT, firstname TEXT, 
             lastname TEXT, email TEXT, gender TEXT, birthDate TEXT)''')

# Function to read CSV and store data in the database
def read_csv_and_store(dataset.csv):
    with open(dataset.csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            c.execute("INSERT INTO clients (category, firstname, lastname, email, gender, birthDate) VALUES (?, ?, ?, ?, ?, ?)",
                      (row['category'], row['firstname'], row['lastname'], row['email'], row['gender'], row['birthDate']))
        conn.commit()

# Function to filter data
def filter_data(category=None, gender=None, dob=None, age=None, age_range=None):
    query = "SELECT * FROM clients WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if gender:
        query += " AND gender = ?"
        params.append(gender)

    if dob:
        query += " AND birthDate = ?"
        params.append(dob)

    if age:
        today = datetime.now()
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        calculated_age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        if calculated_age == age:
            return c.execute(query, params).fetchall()

    if age_range:
        start_age, end_age = map(int, age_range.split('-'))
        today = datetime.now()
        start_date = today.replace(year=today.year - end_age)
        end_date = today.replace(year=today.year - start_age)
        query += " AND birthDate BETWEEN ? AND ?"
        params.append(start_date.strftime('%Y-%m-%d'))
        params.append(end_date.strftime('%Y-%m-%d'))

    return c.execute(query, params).fetchall()

# Function to export filtered data to CSV
def export_to_csv(data, dataset.csv):
    with open(dataset.csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['category', 'firstname', 'lastname', 'email', 'gender', 'birthDate'])
        writer.writerows(data)

# API Routes
@app.route('/filter', methods=['GET'])
def filter_api():
    category = request.args.get('category')
    gender = request.args.get('gender')
    dob = request.args.get('dob')
    age = request.args.get('age', type=int)
    age_range = request.args.get('age_range')

    filtered_data = filter_data(category, gender, dob, age, age_range)
    return jsonify(filtered_data)

@app.route('/export', methods=['GET'])
def export_api():
    category = request.args.get('category')
    gender = request.args.get('gender')
    dob = request.args.get('dob')
    age = request.args.get('age', type=int)
    age_range = request.args.get('age_range')

    filtered_data = filter_data(category, gender, dob, age, age_range)
    export_to_csv(filtered_data, 'app/exported_data.csv')
    return 'Data exported successfully.'

# Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Dataset API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    read_csv_and_store('app/dataset.csv')
    app.run(debug=True, host='0.0.0.0')
