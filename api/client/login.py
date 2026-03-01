from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import bcrypt

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login_api():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No data provided"})

        email = data.get("email")
        password = data.get("password")

        # ---------------- Validation ----------------
        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password required"
            })

        conn = get_connection()
        if not conn:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            })

        cursor = conn.cursor()

        # ---------------- Fetch User ----------------
        cursor.execute(
            "SELECT password,is_verified,username FROM clients WHERE email=%s",
            (email,)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({
                "success": False,
                "message": "User not found"
            })

        db_password = result[0]
        is_verified = result[1]
        name = result[2]

        # ---------------- Fix password type issue ----------------
        if isinstance(db_password, str):
            db_password = db_password.encode("utf-8")

        # ---------------- Check Password ----------------
        if not bcrypt.checkpw(password.encode("utf-8"), db_password):
            return jsonify({
                "success": False,
                "message": "Invalid password"
            })

        # ---------------- Check Verification ----------------
        if not is_verified:
            return jsonify({
                "success": False,
                "message": "Account not verified"
            })

        # ---------------- Success ----------------
        return jsonify({
            "success": True,
            "message": "Login successful",
            "name": name,
            "redirect": "/dashboard"
        })

    except Exception as e:
        print("❌ Login Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        })
    finally:
        try:
            conn.close()
        except:
            pass
