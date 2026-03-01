from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection

update_request_status_bp = Blueprint("update_request_status", __name__)

@update_request_status_bp.route("/update-request-status", methods=["PUT"])
def update_request_status():
    try:
        data = request.get_json()

        # ---------------- Validate JSON ----------------
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid JSON body"
            }), 400

        lawyer_name = data.get("lawyer_name")
        request_id = data.get("request_id")
        status = data.get("status")

        if not lawyer_name or not request_id or not status:
            return jsonify({
                "success": False,
                "message": "lawyer_name, request_id and status are required"
            }), 400

        if status not in ["accepted", "rejected"]:
            return jsonify({
                "success": False,
                "message": "Status must be 'accepted' or 'rejected'"
            }), 400

        conn = get_connection()
        if not conn:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = conn.cursor()

        # ---------------- Get Lawyer ID from Name ----------------
        cursor.execute(
            "SELECT id FROM lawyers WHERE name = %s",
            (lawyer_name,)
        )
        lawyer = cursor.fetchone()

        if not lawyer:
            return jsonify({
                "success": False,
                "message": "Lawyer not found"
            }), 404

        lawyer_id = lawyer[0]

        # ---------------- Check Request ----------------
        cursor.execute("""
            SELECT status FROM client_requests
            WHERE id=%s AND lawyer_id=%s
        """, (request_id, lawyer_id))

        request_data = cursor.fetchone()

        if not request_data:
            return jsonify({
                "success": False,
                "message": "Request not found or does not belong to this lawyer"
            }), 404

        current_status = request_data[0]

        if current_status != "Pending":
            return jsonify({
                "success": False,
                "message": f"Request already {current_status}"
            }), 400

        # ---------------- Update Status ----------------
        cursor.execute("""
            UPDATE client_requests
            SET status=%s
            WHERE id=%s
        """, (status, request_id))

        conn.commit()

        return jsonify({
            "success": True,
            "request_id": request_id,
            "lawyer_name": lawyer_name,
            "updated_status": status
        }), 200

    except Exception as e:
        print("❌ Update Request Status Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        try:
            conn.close()
        except:
            pass
