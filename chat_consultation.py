from flask import Flask, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
from pymongo import MongoClient
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

# Initialize SocketIO for real-time messaging
socketio = SocketIO(app, cors_allowed_origins="*")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["familiar_care"]
chats_collection = db["chats"]

# Store active chat rooms
active_rooms = {}

# -------------------- Chat API Routes --------------------

@app.route("/start_chat", methods=["POST"])
def start_chat():
    """
    Starts a new chat session between user and vet.
    """
    data = request.json
    user_id = data["user_id"]
    vet_id = data["vet_id"]
    room_id = f"chat_{user_id}_{vet_id}"

    if room_id not in active_rooms:
        active_rooms[room_id] = {"user": user_id, "vet": vet_id, "messages": []}

    return jsonify({"room_id": room_id, "message": "Chat started successfully"}), 200


@socketio.on("join")
def handle_join(data):
    """
    Allows user/vet to join a chat room.
    """
    room = data["room"]
    join_room(room)
    send(f"User has joined the chat: {room}", room=room)


@socketio.on("send_message")
def handle_message(data):
    """
    Handles message sending and stores it in MongoDB.
    """
    room = data["room"]
    sender = data["sender"]
    message = data["message"]
    timestamp = datetime.datetime.utcnow()

    chat_data = {
        "room": room,
        "sender": sender,
        "message": message,
        "timestamp": timestamp
    }
    chats_collection.insert_one(chat_data)

    send({"sender": sender, "message": message, "timestamp": str(timestamp)}, room=room)


@socketio.on("leave")
def handle_leave(data):
    """
    Allows user/vet to leave a chat room.
    """
    room = data["room"]
    leave_room(room)
    send(f"User has left the chat: {room}", room=room)


@app.route("/chat_history", methods=["GET"])
def get_chat_history():
    """
    Retrieves chat history for a specific room.
    """
    room = request.args.get("room")
    messages = list(chats_collection.find({"room": room}, {"_id": 0}))
    return jsonify(messages), 200


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
