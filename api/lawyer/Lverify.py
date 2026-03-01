from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection

verify_lawyer_bp = Blueprint("verify_lawyer", __name__)

@verify_lawyer_bp.route("/verify-lawyer", methods=["POST"])
def verify_lawyer():
    email = request.args.get("email")  # Email comes from URL
    data = request.get_json()
    code = data.get("code")

    if not email or not code:
        return jsonify({"success": False, "message": "Email and code are required"})

    conn = get_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"})

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT verification_code, is_verified FROM lawyers WHERE email=%s", (email,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"success": False, "message": "Email not found"})

        db_code, is_verified = result

        if is_verified:
            return jsonify({"success": True, "message": "Account already verified", "redirect": "/Ldash"})

        if db_code == code:
            cursor.execute("UPDATE lawyers SET is_verified=1 WHERE email=%s", (email,))
            conn.commit()
            return jsonify({"success": True, "message": "Verification successful", "redirect": "/Llogin"})
        else:
            return jsonify({"success": False, "message": "Invalid verification code"})
    except Exception as e:
        print(f"❌ Lawyer Verification Error: {e}")
        return jsonify({"success": False, "message": "Server error"})
    finally:
        conn.close()
# -*- coding: utf-8 -*-

