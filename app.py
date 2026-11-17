from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(MONGO_URI)
db = client["todo_database"]
todos = db["todos"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api():
    return jsonify({"message": "Todo API is running"})

@app.route("/submitTodoItem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data required"}), 400

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({
            "error": "Item name and description are required"
        }), 400

    todo = {
        "itemName": item_name,
        "itemDescription": item_description,
        "createdAt": datetime.utcnow()
    }

    result = todos.insert_one(todo)

    return jsonify({
        "message": "Item saved successfully",
        "id": str(result.inserted_id)
    }), 201

if __name__ == "__main__":
    app.run(debug=True)