from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Language mapping (safe for Piston)
LANG_MAP = {
    "python": "python",
    "javascript": "javascript",
    "cpp": "cpp",
    "java": "java"
}

@app.route('/run', methods=['POST'])
def run_code():
    try:
        data = request.json

        language = LANG_MAP.get(data.get('language'), "python")
        code = data.get('code', '')

        payload = {
            "language": language,
            "version": "*",
            "files": [{"content": code}]
        }

        response = requests.post(
            "https://emkc.org/api/v2/piston/execute",
            json=payload,
            timeout=10
        )

        result = response.json()

        run_data = result.get("run", {})
        output = run_data.get("output", "")
        stderr = run_data.get("stderr", "")

        final_output = output if output else stderr
        if not final_output:
            final_output = "No Output"

        return jsonify({"output": final_output})

    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)