import helpers

from google.cloud import language_v2
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

PROJECT_ID = "happi-415103"
assert PROJECT_ID
PARENT = f"projects/{PROJECT_ID}"
SENTIMENT_SCORE_CLIENT = language_v2.LanguageServiceClient()

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
    skill = query['skill']
    equipment = query['equipment']
    sleep_goal = query['sleep_goal']
    wakeup_time = query['wakeup_time']
    
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    data = {
        "user_id": user_id,
        "first": first_name,
        "last": last_name,
        "email": email,
        "exercise_info": {
            "exercise_goal": exercise_goal,
            "skill": skill,
            "equipment": equipment
        },
        "sleep_info": {
            "sleep_goal": sleep_goal,
            "wakeup_time": wakeup_time
        },
        "journal_info": {
            "happiness_score": 0,
            "journal_entry": ""
        }
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
    
@app.route('/journal', methods=['GET'])
def journal():
    query = request.args.to_dict()
    user_id = query['user_id']
    text_content = query['entry']
    
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
    
    language_code = "en"
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    encoding_type = language_v2.EncodingType.UTF8

    response = SENTIMENT_SCORE_CLIENT.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    
    score = response.document_sentiment.score
    
    data_to_update = {
        "journal_info": {
            "happiness_score": score,
            "journal_entry": text_content
        }
    }
    
    db.collection("users").document(user_id).update(data_to_update)
    
    return jsonify({'exit_status': 0, 'score': score})

@app.route('/fitness', methods=['GET'])
def fitness():
    query = request.args.to_dict()
    user_id = query['user_id']
    body_part = query['body_part']
    exercise_type = query['exercise_type']
    
    user_query = db.collection("users").where("user_id", "==", user_id).limit(1).get()
    
    if not user_query:
        return jsonify({'exit_status': -1})
    
    skill = user_query[0].to_dict().get("exercise_info", {}).get('skill')
    equipment = user_query[0].to_dict().get("exercise_info", {}).get('equipment')
    
    user_query = db.collection("exercises").where("BodyPart", "==", body_part).where("Level", "==", skill).where("Type", "==", exercise_type).where("Equipment", "in", equipment).limit(20).get()
    
    if not user_query:
        return jsonify({'exit_status': -1})
    
    exercise_data = []
    for doc in user_query:
        exercise_data.append(doc.to_dict())
        
    return jsonify({'exit_status': 0, 'exercise_data': exercise_data})

@app.route('/sleep', methods=['GET'])
def sleep():
    query = request.args.to_dict()
    user_id = query['user_id']
    user_query = db.collection("users").where("user_id", "==", user_id).limit(1).get()
    
    if not user_query:
        return jsonify({'exit_status': -1})
    
    awakeTime = user_query[0].to_dict().get("sleep_info", {}).get('wakeup_time')
    wakeUpTimes = []
    track = 2
    for x in range(3):
        wakeUpTimes[x] = awakeTime - (6 + (1.5 * track))
        track -= 1
        if wakeUpTimes[x] < 0:
            wakeUpTimes[x] = 24 + wakeUpTimes[x]
    
    return jsonify({'exit_status': 0, 'wakeup_times': wakeUpTimes})

if __name__ == '__main__':
    # app.run()
    pass