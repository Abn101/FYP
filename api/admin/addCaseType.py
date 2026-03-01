# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import pymysql

add_case_bp = Blueprint("add_case", __name__)

@add_case_bp.route("/case-types", methods=["POST"])
def add_case_type():
    data = request.get_json()

    case_name = data.get("case_name")
    description = data.get("description")

    # ---------------- Validation ----------------
    if not case_name:
        return jsonify({
            "success": False,
            "message": "Case name is required"
        })

    conn = get_connection()
    if not conn:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        })

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Check duplicate case name
        cursor.execute(
            "SELECT id FROM case_types WHERE case_name=%s",
            (case_name,)
        )
        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Case type already exists"
            })

        # Insert new case type
        cursor.execute(
            """
            INSERT INTO case_types (case_name, description)
            VALUES (%s, %s)
            """,
            (case_name, description)
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Case type added successfully"
        })

    except Exception as e:
        print("❌ Add Case Type Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        })

    finally:
        conn.close()
