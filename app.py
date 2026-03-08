from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load variables from a .env file if it exists (for local testing)
load_dotenv()

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Use the local URI from your Compass for now, or an Env Var for Render
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Accessing the database and collection seen in your Compass
db = client['haircare_db']
collection = db['user_analysis']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/questions")
def questions():
    return render_template("questions.html")

@app.route("/result")
def result():
    return render_template("result.html")

# New Route to save the quiz data to MongoDB
@app.route("/api/save-analysis", methods=["POST"])
def save_analysis():
    try:
        data = request.json  # Get the hair analysis data from your JS
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Insert the data into the user_analysis collection
        result = collection.insert_one(data)
        return jsonify({"message": "Success", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Get port from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Check if we are in production or local
    # If "RENDER" is in environment, set debug to False
    is_dev = not os.environ.get("RENDER")
    
    app.run(host="0.0.0.0", port=port, debug=is_dev)