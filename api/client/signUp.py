from flask import Blueprint, request, jsonify
import bcrypt
import random
from dbOperations.dbConn import get_connection
import smtplib
from email.mime.text import MIMEText

# ------------------------- Blueprint -------------------------
signup_bp = Blueprint("signup", __name__)

# ------------------------- Email function -------------------------
def send_email(to_email, code):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "f2021266406@umt.edu.pk"
    sender_password = "ailruuhkatosdgsz"

    subject = "Welcome to FYP App"
    body = f"Your signup is successful! Your 4-digit verification code is: {code}"

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
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ------------------------- Signup API -------------------------
@signup_bp.route("/signup", methods=["POST"])
def signup_api():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # ---------------------- Validation ----------------------
    if not name or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"})

    conn = get_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"})

    cursor = conn.cursor()

    # ---------------------- Check duplicates ----------------------
    cursor.execute("SELECT id FROM clients WHERE email=%s", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "Email already exists"})

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    special_code = f"{random.randint(1000, 9999)}"

    try:
        cursor.execute(
            "INSERT INTO clients (username, email, password, special_code, is_verified) VALUES (%s, %s, %s, %s, 0)",
            (name, email, hashed_password, special_code)
        )
        conn.commit()

        send_email(email, special_code)

        return jsonify({
            "success": True,
            "redirect": f"/verify?email={email}"
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"success": False, "message": "Database error"})
    finally:
        conn.close()
