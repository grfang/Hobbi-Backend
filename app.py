from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import psycopg2
import random
import string

app = Flask(__name__)
CORS(app)

DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'hobbi'

conn = psycopg2.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

cursor = conn.cursor()

@app.route('/', methods=['GET'])
def signup():
    query = request.args.to_dict()
    email = query['emails']
    firstname = query['firstname']
    lastname = query['lastname']
    
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return jsonify({'user_id': user_id})

if __name__ == '__main__':
    app.run()