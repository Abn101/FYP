from flask import Blueprint, jsonify
from dbOperations.dbConn import get_connection
import pymysql

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/case-types", methods=["GET"])
def get_case_types():
    conn = get_connection()
    if not conn:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        })

    # ✅ Correct way for PyMySQL
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id, case_name, description FROM case_types")
        results = cursor.fetchall()

        if not results:
            return jsonify({
                "success": True,
                "case_types": [],
                "message": "No case types available"
            })

        return jsonify({
            "success": True,
            "case_types": results
        })

    except Exception as e:
        print("❌ Dashboard Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        })
    finally:
        conn.close()
