# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection

client_request_bp = Blueprint("client_request", __name__)

@client_request_bp.route("/client-request", methods=["POST"])
def create_client_request():
    data = request.get_json()

    client_name = data.get("client_name")
    lawyer_name = data.get("lawyer_name")
    case_type_name = data.get("case_type_name")
    description = data.get("description")

    # ---------------- Validation ----------------
    if not client_name or not lawyer_name or not case_type_name or not description:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    conn = get_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Get client id
        cursor.execute("SELECT id FROM clients WHERE username=%s", (client_name,))
        client = cursor.fetchone()
        if not client:
            return jsonify({"success": False, "message": f"Client '{client_name}' not found"}), 404
        client_id = client[0]

        # Get case type id
        cursor.execute("SELECT id FROM case_types WHERE case_name=%s", (case_type_name,))
        case_type = cursor.fetchone()
        if not case_type:
            return jsonify({"success": False, "message": f"Case type '{case_type_name}' not found"}), 404
        case_type_id = case_type[0]

        # Get lawyer id and check case type
        cursor.execute("SELECT id, case_type_id FROM lawyers WHERE name=%s", (lawyer_name,))
        lawyer = cursor.fetchone()
        if not lawyer:
            return jsonify({"success": False, "message": f"Lawyer '{lawyer_name}' not found"}), 404
        lawyer_id, lawyer_case_type_id = lawyer

        # Validate lawyer handles this case type
        if lawyer_case_type_id != case_type_id:
            return jsonify({"success": False, "message": f"Lawyer '{lawyer_name}' does not handle '{case_type_name}'"}), 400

        # Insert request
        cursor.execute(
            "INSERT INTO client_requests (client_id, lawyer_id, case_type_id, description) VALUES (%s, %s, %s, %s)",
            (client_id, lawyer_id, case_type_id, description)
        )
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Request submitted successfully",
            "client_name": client_name,
            "lawyer_name": lawyer_name,
            "case_type_name": case_type_name
        })

    except Exception as e:
        print("❌ Client Request Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        conn.close()
