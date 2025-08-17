from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CORS(app)

# MongoDB configuration using environment variables
mongo_url = os.getenv('MONGO_URL3')
mongo_db = os.getenv('MONGO_DB3')
mongo_collection = os.getenv('MONGO_COLLECTION3')

if not mongo_url or not mongo_db or not mongo_collection:
    raise ValueError("Missing MongoDB configuration in environment variables")

try:
    client = MongoClient(mongo_url) 
    db = client[mongo_db]
    collection = db[mongo_collection]
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

def get_user_identifier():
    if request.form.get('username'):
        return request.form.get('username')
    else:
        return get_remote_address()

limiter = Limiter(
    key_func=get_user_identifier,
    app=app,
    default_limits=["5 per minute"]
)

#Routes
@app.route('/')
def welcome():
    return "Nothing to see here"

# Authentication Logic
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute") 
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = collection.find_one({'username': username})

    if user:
        if user['password'] == password:
            return jsonify({'authenticated': True}), 200
        else:
            return jsonify({'error': 'Invalid Credentials'}), 401
    else:
        return jsonify({'error': 'Invalid Credentials'}), 401
    
    
#Handling rate limit
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Too Many request from this user, Try after 1 minute"), 429


# Retrieve documents
@app.route('/document', methods = ['GET'])
def getdocs():
    try:
        credentials = list(collection.find({},{'_id':0}))
        return jsonify(credentials)
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return jsonify({"error": "Failed to retrieve documents"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
        