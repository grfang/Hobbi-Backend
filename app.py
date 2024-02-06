from flask import Flask, jsonify, request
from flask_cors import CORS
import json
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
@app.route('/', methods=['GET'])
def signup():
    query = request.args.to_dict()
    email = query['emails']
    firstname = query['firstname']
    lastname = query['lastname']
    
    user_id = "what"
    
    return jsonify({'user_id': user_id})

if __name__ == '__main__':
    # app.run()
    doc_ref = db.collection("users").document("testUser")
    doc_ref.set({"first": "Gia", "last": "Fang", "email": "giafang@gmail.com", "stepgoal": 10000})
    doc_ref = db.collection("users").document("testUser2")
    doc_ref.set({"first": "Alan", "last": "Turing", "email": "turing@gmail.com", "stepgoal": 10000})
    
    # print('Reading exercises.json')
    # records = None
    # with open('exercises.json', encoding="utf-8") as json_file:  
    #     records = json.load(json_file)
    # print('%i records read from file' % len(records))

    # i = 0
    # batch = db.batch()
    # print('Writing records to Firestore')
    # for record in records:
    #     doc = db.collection('exercises').document(record['field1'])
    #     batch.set(doc, record)
    #     i += 1
    #     if (i % 500 == 0):
    #         batch.commit()
    #         batch = db.batch()
    #         print(i)
    # batch.commit()
    # print(i)
    pass