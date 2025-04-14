# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.exporter.prometheus import PrometheusMetricReader
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# from opentelemetry import metrics

# from opentelemetry.instrumentation.django import DjangoInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.instrumentation.mysql import MySQLInstrumentor
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor



# def setup_telemetry():
#     resource = Resource.create({"service_name": "projectmanagement"})
#     tracer_provider = TracerProvider(resource=resource)

#     # Add Console Exporter
#     console_exporter = ConsoleSpanExporter()
#     span_processor = SimpleSpanProcessor(console_exporter)
#     tracer_provider.add_span_processor(span_processor)

#     # Set the tracer provider globally
#     trace.set_tracer_provider(tracer_provider)

#     # Setup metrics
#     prometheus_reader = PrometheusMetricReader()
#     meter_provider = MeterProvider(
#         metric_readers=[prometheus_reader], resource=resource
#     )
#     # metrics.set_meter_provider(meter_provider)

#     # Instrument
#     DjangoInstrumentor().instrument()
#     RequestsInstrumentor().instrument()
#     MySQLInstrumentor().instrument()

#     return prometheus_reader



# telemetry.py

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from prometheus_client import start_http_server, Histogram
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
# Global variables
meter = None
request_duration_histogram = None
_telemetry_initialized = False

def setup_telemetry():
    global meter, request_duration_histogram, _telemetry_initialized

    if _telemetry_initialized:
        return  # Avoid reinitializing
    _telemetry_initialized = True

    # Define telemetry resource (optional, but recommended)
    resource = Resource(attributes={
        "service.name": "project-management"
    })

    # Set up Tracer
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Export spans to console and optionally OTLP
    span_processor = BatchSpanProcessor(ConsoleSpanExporter())
    tracer_provider.add_span_processor(span_processor)

    # OTLP exporter (optional if you're using Grafana Tempo or similar)
    # otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces", insecure=True)
    # tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Set up Meter
    metric_exporter = OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")
    reader = PeriodicExportingMetricReader(metric_exporter)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    # Start Prometheus metrics HTTP server on custom port (avoid conflicts)
    try:
        start_http_server(port=8000, addr="0.0.0.0")  # <- change this port if needed
    except OSError as e:
        print(f"Prometheus HTTP server error: {e}")

    meter = metrics.get_meter(__name__)
    request_duration_histogram = Histogram(
        "request_duration_seconds",
        "Duration of HTTP requests in seconds",
        buckets=(0.1, 0.5, 1, 2, 5)
    )

class TelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        DjangoInstrumentor().instrument()

    def __call__(self, request):
        response = self.get_response(request)
        return respons