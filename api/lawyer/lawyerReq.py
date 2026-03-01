# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import pymysql

fetch_lawyer_requests_bp = Blueprint("fetch_lawyer_requests", __name__)

@fetch_lawyer_requests_bp.route("/lawyer-requests-by-name", methods=["GET"])
def get_requests_by_lawyer_name():
    lawyer_name = request.args.get("name")

    # ---------------- Validation ----------------
    if not lawyer_name:
        return jsonify({
            "success": False,
            "message": "Lawyer name is required"
        })

    conn = get_connection()
    if not conn:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        })

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 1️⃣ Check if lawyer exists
        cursor.execute(
            "SELECT id FROM lawyers WHERE name=%s",
            (lawyer_name,)
        )
        lawyer = cursor.fetchone()

        if not lawyer:
            return jsonify({
                "success": False,
                "message": "Lawyer not found"
            })

        lawyer_id = lawyer["id"]

        # 2️⃣ Fetch client requests belonging to this lawyer
        cursor.execute("""
            SELECT 
            cr.id,
                c.username AS client_name,
                ct.case_name AS case_type_name,
                cr.description,
                cr.status
            FROM client_requests cr
            JOIN clients c ON cr.client_id = c.id
            JOIN case_types ct ON cr.case_type_id = ct.id
            WHERE cr.lawyer_id = %s
        """, (lawyer_id,))

        requests = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": requests
        })

    except Exception as e:
        print("❌ Fetch Lawyer Requests Error:", e)
        return jsonify({
            "success": False,
            "message": str(e)
        })

    finally:
        conn.close()
