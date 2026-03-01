from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room

from api.client.signUp import signup_bp
from api.client.verify import verify_bp
from api.client.login import login_bp
from api.client.cdash import dashboard_bp
from api.admin.addCaseType import add_case_bp
from api.lawyer.lawyerSignup import lawyer_signup_bp
from dbOperations.creation import createLaywyer
from api.lawyer.Lverify import verify_lawyer_bp
from api.lawyer.Llogin import lawyer_login_bp
from api.lawyer.fetchLawyerType import fetch_lawyer_bp
from api.client.clientReq import client_request_bp
from api.client.fetchReq import fetch_client_requests_bp
from api.lawyer.lawyerReq import fetch_lawyer_requests_bp
from api.lawyer.acceptreject import update_request_status_bp
from api.messeaging.sendMessage import send_chat_bp
from api.messeaging.reciveMessage import recive_chat_bp
from api.lawyer.lawyerchatbot import lawyer_chatbot_bp
from api.admin.fetch import fetch_case_types_bp
# Create tables
createLaywyer()

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

# 🔥 Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- REGISTER BLUEPRINTS ----------------
app.register_blueprint(signup_bp)
app.register_blueprint(verify_bp)
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(add_case_bp)
app.register_blueprint(lawyer_signup_bp)
app.register_blueprint(verify_lawyer_bp)
app.register_blueprint(lawyer_login_bp)
app.register_blueprint(fetch_lawyer_bp)
app.register_blueprint(client_request_bp)
app.register_blueprint(fetch_client_requests_bp)
app.register_blueprint(fetch_lawyer_requests_bp)
app.register_blueprint(update_request_status_bp)
app.register_blueprint(send_chat_bp)
app.register_blueprint(recive_chat_bp)
app.register_blueprint(lawyer_chatbot_bp)
app.register_blueprint(fetch_case_types_bp)

# ---------------- SOCKET EVENTS ----------------
@socketio.on("join")
def handle_join(data):
    request_id = data.get("request_id")
    if request_id:
        join_room(str(request_id))

@socketio.on("leave")
def handle_leave(data):
    request_id = data.get("request_id")
    if request_id:
        leave_room(str(request_id))

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    socketio.run(app, debug=True)
