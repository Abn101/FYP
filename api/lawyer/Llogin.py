# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import bcrypt

lawyer_login_bp = Blueprint("lawyer_login", __name__)

@lawyer_login_bp.route("/lawyer-login", methods=["POST"])
def lawyer_login():
    try:
        data = request.get_json()

        # ---------------- Validate JSON ----------------
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid or missing JSON body"
            }), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400

        # ---------------- Database Connection ----------------
        conn = get_connection()
        if not conn:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = conn.cursor()

        # ✅ Fetch name also
        cursor.execute(
            "SELECT id, name, password, is_verified FROM lawyers WHERE email=%s",
            (email,)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({
                "success": False,
                "message": "Lawyer not found"
            }), 404

        lawyer_id, name, db_password, is_verified = result

        # ---------------- Fix Password Type ----------------
        if isinstance(db_password, str):
            db_password = db_password.encode("utf-8")

        # ---------------- Check Password ----------------
        if not bcrypt.checkpw(password.encode("utf-8"), db_password):
            return jsonify({
                "success": False,
                "message": "Invalid password"
            }), 401

        # ---------------- Check Verification ----------------
        if not is_verified:
            return jsonify({
                "success": False,
                "message": "Account not verified"
            }), 403

        # ---------------- Success ----------------
        return jsonify({
            "success": True,
            "message": "Login successful",
            "lawyer_id": lawyer_id,
            "name": name,
        }), 200

    except Exception as e:
        print("❌ Lawyer Login Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        try:
            conn.close()
        except:
            pass
