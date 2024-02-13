import helpers

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pprint import pprint
import random
import string

from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("./service-account.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

load_dotenv()

#flask setup
app = Flask(__name__)
CORS(app)

#routes
@app.route('/signup', methods=['POST'])
def signup_route():
    query = request.args.to_dict()
    email = query['emails']
    first_name = query['firstname']
    last_name = query['lastname']
    exercise_goal = query['exercise_goal']
    sleep_goal = query['exercise_goal']
    
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    data = {
        "user_id": user_id,
        "first": first_name,
        "last": last_name,
        "email": email,
        "goals": {
            "exercise": exercise_goal,
            "sleep": sleep_goal
        },
        "happiness_score": 0,
        "journal_entry": ""
    }
    
    db.collection("users").document(user_id).set(data)
    
    return jsonify({'exit_status': 0, 'user_id': user_id})

@app.route('/login', methods=['GET'])
def login():
    query = request.args.to_dict()
    email = query['emails']
    
    user_query = db.collection("users").where("email", "==", email).limit(1).get()

    if not user_query:
        return jsonify({'exit_status': -1})
    else:
        user_id = user_query[0].id
        return jsonify({'exit_status': 0, 'user_id': user_id})
    
@app.route('/data', methods=['GET'])
def get_user_data():
    query = request.args.to_dict()
    user_id = query['user_id']
    
    user_query = db.collection("users").where("user_id", "==", user_id).limit(1).get()
    
    if not user_query:
        return jsonify({'exit_status': -1})
    else:
        user_data = user_query[0].to_dict()
        return jsonify({'exit_status': 0, 'data': user_data})

if __name__ == '__main__':
    # app.run()
    pass