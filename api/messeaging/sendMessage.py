from flask import Blueprint, request, jsonify, current_app
from dbOperations.dbConn import get_connection
import pymysql

send_chat_bp = Blueprint("chat", __name__)

@send_chat_bp.route("/send-message", methods=["POST"])
def send_message():
    conn = None
    try:
        data = request.get_json()

        request_id = data.get("request_id")
        sender_type = data.get("sender_type")   # client / lawyer
        sender_name = data.get("sender_name")   # name instead of id
        message = data.get("message")

        # ---------------- Validation ----------------
        if not request_id or not sender_type or not sender_name or not message:
            return jsonify({
                "success": False,
                "message": "All fields required"
            }), 400

        if sender_type not in ["client", "lawyer"]:
            return jsonify({
                "success": False,
                "message": "Invalid sender type"
            }), 400

        conn = get_connection()
        if not conn:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # ---------------- Get Request Info ----------------
        cursor.execute(
            "SELECT client_id, lawyer_id, status FROM client_requests WHERE id=%s",
            (request_id,)
        )
        req = cursor.fetchone()

        if not req:
            return jsonify({
                "success": False,
                "message": "Request not found"
            }), 404

        if req["status"] != "Accepted":
            return jsonify({
                "success": False,
                "message": "Chat allowed only after acceptance"
            }), 403

        # ---------------- Get Sender ID ----------------
        if sender_type == "client":
            cursor.execute(
                "SELECT id FROM clients WHERE username=%s",
                (sender_name,)
            )
            sender = cursor.fetchone()

            if not sender:
                return jsonify({
                    "success": False,
                    "message": "Client not found"
                }), 404

            sender_id = sender["id"]

            if sender_id != req["client_id"]:
                return jsonify({
                    "success": False,
                    "message": "Unauthorized client"
                }), 403

        else:  # lawyer
            cursor.execute(
                "SELECT id FROM lawyers WHERE name=%s",
                (sender_name,)
            )
            sender = cursor.fetchone()

            if not sender:
                return jsonify({
                    "success": False,
                    "message": "Lawyer not found"
                }), 404

            sender_id = sender["id"]

            if sender_id != req["lawyer_id"]:
                return jsonify({
                    "success": False,
                    "message": "Unauthorized lawyer"
                }), 403

        # ---------------- Insert Message ----------------
        cursor.execute("""
            INSERT INTO chat_messages (request_id, sender_type, sender_id, message)
            VALUES (%s, %s, %s, %s)
        """, (request_id, sender_type, sender_id, message))

        conn.commit()

        # 🔥 ---------------- SOCKET EMIT ----------------
        # This sends message instantly to all users in that request room
        current_app.extensions["socketio"].emit(
            "new_message",
            {
                "request_id": request_id,
                "sender_type": sender_type,
                "sender_name": sender_name,
                "message": message
            },
            room=str(request_id)
        )
        # ------------------------------------------------

        return jsonify({
            "success": True,
            "message": "Message sent successfully",
            "sender_name": sender_name,
            "sender_type": sender_type
        }), 200

    except Exception as e:
        print("❌ Chat Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        if conn:
            conn.close()
