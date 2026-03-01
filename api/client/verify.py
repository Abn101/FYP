# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import smtplib
from email.mime.text import MIMEText

verify_bp = Blueprint("verify", __name__)

# ------------------------- Email Function -------------------------
def send_verification_email(to_email, code):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "f2021266406@umt.edu.pk"
    sender_password = "ailruuhkatosdgsz"  # Your App Password

    subject = "FYP Signup Verification"
    body = f"Your verification code is: {code}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Verification email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send verification email: {e}")

# ------------------------- Verify API -------------------------
@verify_bp.route("/verify", methods=["POST"])
def verify_api():
    data = request.get_json()
    email = request.args.get("email")
    code = data.get("code")

    if not email or not code:
        return jsonify({"success": False, "message": "Email and code are required"})

    conn = get_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"})

    cursor = conn.cursor()
    try:
        # Get the special_code from DB
        cursor.execute("SELECT special_code FROM clients WHERE email=%s", (email,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"success": False, "message": "Email not found"})

        db_code = result[0]
        if db_code == code:
            # Update user as verified
            cursor.execute("UPDATE clients SET is_verified=1 WHERE email=%s", (email,))
            conn.commit()
            return jsonify({"success": True, "redirect": "/login"})
        else:
            return jsonify({"success": False, "message": "Invalid verification code"})
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"success": False, "message": "Database error"})
    finally:
        conn.close()
