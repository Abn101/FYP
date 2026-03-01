from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import pymysql

fetch_client_requests_bp = Blueprint("fetch_client_requests", __name__)

@fetch_client_requests_bp.route("/client-requests-by-name", methods=["GET"])
def get_client_requests_by_name():
    client_name = request.args.get("client_name")

    # ---------------- Validation ----------------
    if not client_name:
        return jsonify({
            "success": False,
            "message": "Client name is required"
        })

    conn = get_connection()
    if not conn:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        })

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Check if client exists
        cursor.execute(
            "SELECT id FROM clients WHERE username=%s",
            (client_name,)
        )
        client = cursor.fetchone()

        if not client:
            return jsonify({
                "success": False,
                "message": "Client not found"
            })

        client_id = client["id"]

        # Fetch client requests
        cursor.execute("""
            SELECT 
            cr.id,
                c.username AS client_name,
                l.name AS lawyer_name,
                ct.case_name AS case_type_name,
                cr.description,
                cr.status
            FROM client_requests cr
            JOIN clients c ON cr.client_id = c.id
            JOIN lawyers l ON cr.lawyer_id = l.id
            JOIN case_types ct ON cr.case_type_id = ct.id
            WHERE cr.client_id = %s
        """, (client_id,))

        requests = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": requests
        })

    except Exception as e:
        print("❌ Fetch Client Requests Error:", e)
        return jsonify({
            "success": False,
            "message": str(e)  # shows real error for debugging
        })

    finally:
        conn.close()
