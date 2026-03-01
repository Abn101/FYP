# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from dbOperations.dbConn import get_connection
import pymysql

fetch_lawyer_bp = Blueprint("fetch_lawyer", __name__)

@fetch_lawyer_bp.route("/lawyers-by-case-name", methods=["GET"])
def get_lawyers_by_case_name():
    # Get case_type_name from query params
    case_type_name = request.args.get("case_type_name")
    if not case_type_name:
        return jsonify({"success": False, "message": "case_type_name is required"})

    conn = get_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"})

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # First, fetch the case_type_id for the given name
        cursor.execute(
            "SELECT id FROM case_types WHERE case_name=%s",
            (case_type_name,)
        )
        case_type = cursor.fetchone()
        if not case_type:
            return jsonify({"success": False, "message": "Case type not found"})

        case_type_id = case_type['id']

        # Fetch lawyers assigned to this case type
        cursor.execute(
            "SELECT id, name, email FROM lawyers WHERE case_type_id=%s",
            (case_type_id,)
        )
        lawyers = cursor.fetchall()

        if not lawyers:
            return jsonify({"success": True, "message": "No lawyers found for this case type", "lawyers": []})

        return jsonify({"success": True, "lawyers": lawyers})

    except Exception as e:
        print(f"❌ Fetch Lawyers Error: {e}")
        return jsonify({"success": False, "message": "Server error"})
    finally:
        conn.close()
