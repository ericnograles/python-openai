from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize the database
    db.init_app(app)

    # Initialize database migrations
    migrate.init_app(app, db)

    # Initialize OpenTelemetry Tracer and Honeycomb exporter
    trace.set_tracer_provider(TracerProvider())
    otlp_exporter = OTLPSpanExporter(
        endpoint="api.honeycomb.io:443",
        insecure=False,
        headers=(
            "x-honeycomb-team={}".format(app.config["HONEYCOMB_API_KEY"]),
            "x-honeycomb-dataset={}".format(app.config["HONEYCOMB_DATASET"]),
        ),
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )

    # Instrument Flask app
    FlaskInstrumentor().instrument_app(app)
    app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)

    # Import and register blueprints
    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    # Import and register error handler
    from .error_handler import handle_unhandled_error
    app.register_error_handler(Exception, handle_unhandled_error)

    return app
