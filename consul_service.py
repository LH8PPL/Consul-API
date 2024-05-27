from flask import Flask, jsonify

app = Flask(__name__)
health_status = "passing"

@app.route('/health', methods=['GET'])
def health():
    if health_status == "passing":
        return jsonify(status="healthy"), 200
    elif health_status == "warning":
        return jsonify(status="warning"), 429
    else:
        return jsonify(status="critical"), 500

@app.route('/set_health/<status>', methods=['POST'])
def set_health(status):
    global health_status
    if status in ["passing", "warning", "critical"]:
        health_status = status
        return jsonify(status="success", message=f"Health status set to {status}"), 200
    else:
        return jsonify(status="error", message="Invalid status"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
