from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import bcrypt, os, random, smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

lawyer_signup_bp = Blueprint("lawyer_signup", __name__)

# ------------------------- Email Function -------------------------
def send_email(to_email, code):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "")
    sender_password = os.getenv("SENDER_PASSWORD", "")

    if not sender_email or not sender_password:
        print("❌ SMTP credentials not configured. Set SENDER_EMAIL and SENDER_PASSWORD.")
        return

    subject = "Lawyer Signup Verification"
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
        print(f"❌ Failed to send email: {e}")

# ------------------------- Signup API -------------------------
@lawyer_signup_bp.route("/lawyer-signup", methods=["POST"])
def lawyer_signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    case_type_name = data.get("case_type")  # Name instead of ID

    # ---------------- Validation ----------------
    if not name or not email or not password or not case_type_name:
        return jsonify({"success": False, "message": "All fields are required"})

    conn = get_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"})

    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM lawyers WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"})

        # Fetch case type id by name
        cursor.execute("SELECT id FROM case_types WHERE case_name=%s", (case_type_name,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"success": False, "message": "Invalid case type"})
        case_type_id = result[0]

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        verification_code = str(random.randint(1000, 9999))

        # Insert lawyer
        cursor.execute(
            "INSERT INTO lawyers (name, email, password, case_type_id, verification_code) VALUES (%s, %s, %s, %s, %s)",
            (name, email, hashed_password, case_type_id, verification_code)
        )
        conn.commit()

        # Send verification email
        send_email(email, verification_code)

        return jsonify({"success": True, "redirect": f"/verify-lawyer?email={email}"})

    except Exception as e:
        print(f"❌ Lawyer Signup Error: {e}")
        return jsonify({"success": False, "message": "Server error"})
    finally:
        conn.close()
