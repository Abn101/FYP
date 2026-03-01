from flask import Blueprint, jsonify
from dbOperations.dbConn import get_connection
import pymysql

fetch_case_types_bp = Blueprint("fetch_case_types", __name__)

@fetch_case_types_bp.route("/case-types", methods=["GET"])
def fetch_case_types():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT id, case_name, description 
            FROM case_types
            ORDER BY case_name ASC
        """)

        case_types = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(case_types),
            "data": case_types
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)   # remove later
        }), 500

    finally:
        if conn:
            conn.close()