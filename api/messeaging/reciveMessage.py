# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from dbOperations.dbConn import get_connection
import pymysql

recive_chat_bp = Blueprint("chat-recive", __name__)

@recive_chat_bp.route("/get-messages/<int:request_id>", methods=["GET"])
def get_messages(request_id):
    conn = None
    try:
        # ---------------- DB Connection ----------------
        conn = get_connection()
        if not conn:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # ---------------- Check Request Exists ----------------
        cursor.execute(
            "SELECT status FROM client_requests WHERE id = %s",
            (request_id,)
        )
        request_data = cursor.fetchone()

        if not request_data:
            return jsonify({
                "success": False,
                "message": "Request not found"
            }), 404

        # ---------------- Allow Chat Only If Accepted ----------------
        if request_data["status"] != "Accepted":
            return jsonify({
                "success": False,
                "message": "Chat available only for accepted requests"
            }), 403

        # ---------------- Fetch Messages ----------------
        cursor.execute("""
            SELECT 
                sender_type,
                sender_id,
                message,
                timestamp
            FROM chat_messages
            WHERE request_id = %s
            ORDER BY timestamp ASC
        """, (request_id,))

        messages = cursor.fetchall()

        return jsonify({
            "success": True,
            "request_id": request_id,
            "messages": messages
        }), 200

    except Exception as e:
        print("❌ Fetch Chat Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        if conn:
            conn.close()
