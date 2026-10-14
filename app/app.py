import json
import logging
import time
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger("sample-app")
started_at = time.time()


@app.before_request
def log_request():
    request.request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())
    )

    logger.info(json.dumps({
        "event": "request_received",
        "request_id": request.request_id,
        "method": request.method,
        "path": request.path
    }))


@app.get("/")
def home():
    return jsonify(
        message="Hello from the EFK logging project"
    )


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/error")
def simulated_error():
    logger.error(json.dumps({
        "event": "simulated_application_error",
        "request_id": request.request_id
    }))

    return jsonify(
        error="Simulated error for logging test"
    ), 500


@app.after_request
def log_response(response):
    logger.info(json.dumps({
        "event": "request_completed",
        "request_id": getattr(request, "request_id", None),
        "path": request.path,
        "status_code": response.status_code
    }))

    return response


@app.get("/metrics-info")
def metrics_info():
    return jsonify(
        uptime_seconds=int(time.time() - started_at)
    )
