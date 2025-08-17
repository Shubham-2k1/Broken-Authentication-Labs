from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
application = app
CORS(app)

# MongoDB configuration using environment variables
mongo_url = os.getenv('MONGO_URL')
mongo_db = os.getenv('MONGO_DB')
mongo_collection = os.getenv('MONGO_COLLECTION')

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

#Routes
@app.route('/')
def home():
    return 'Nothing to see here'

#Authentication Logic
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = collection.find_one({'username': username})

    if user:
        if user['password'] == password:
            return jsonify({'authenticated': True}), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'Invalid username'}), 401
    
# Retrieve documents
@app.route('/document', methods=['GET'])
def get_documents():
    try:
        credential = list(collection.find({},{'_id':0}))
        return jsonify(credential)
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return jsonify({"error": "Failed to retrieve documents"}), 500

if __name__ == '__main__':
    app.run(debug=True)
