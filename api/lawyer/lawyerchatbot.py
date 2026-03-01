# api/lawyer/lawyerchatbot.py

from flask import Blueprint, request, jsonify
import json
import ollama
from model.reterive import retrieve_cases, build_prompt, LLM_MODEL

lawyer_chatbot_bp = Blueprint(
    "lawyer_chatbot",
    __name__,
    url_prefix="/legal"
)

# ---------------- API ROUTE ----------------
@lawyer_chatbot_bp.route("/query", methods=["POST"])
def legal_query():
    try:
        data = request.get_json()
        query = data.get("query") if data else None

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Step 1: Retrieve similar cases
        cases = retrieve_cases(query)

        # Step 2: Build prompt
        prompt = build_prompt(query, cases)

        # Step 3: Get LLM response (non-streaming)
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            "query": query,
            "retrieved_cases": cases,
            "analysis": response["message"]["content"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500