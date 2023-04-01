from flask import jsonify, request
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

def handle_unhandled_error(error):
    # Capture the error details
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("unhandled_error") as span:
        span.set_attribute("error", str(error))
        span.set_attribute("error.type", type(error).__name__)

        # Get the value of the HTTP header (e.g., X-Custom-Header)
        header_value = request.headers.get("X-Custom-Header", None)
        if header_value is not None:
            span.set_attribute("http.header.X-Custom-Header", header_value)

        # You can set the span status to indicate an error
        span.set_status(Status(StatusCode.ERROR, "Unhandled exception"))

    response = {
        "error": "An unexpected error occurred.",
        "details": str(error),
    }
    return jsonify(response), 500
