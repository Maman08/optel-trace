from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry import metrics

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor



def setup_telemetry():
    resource = Resource.create({"service_name": "projectmanagement"})
    tracer_provider = TracerProvider(resource=resource)

    # 👉 Add Console Exporter
    console_exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(console_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Set the tracer provider globally
    trace.set_tracer_provider(tracer_provider)

    # Setup metrics
    prometheus_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(
        metric_readers=[prometheus_reader], resource=resource
    )
    # metrics.set_meter_provider(meter_provider)

    # Instrument
    DjangoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    MySQLInstrumentor().instrument()

    return prometheus_reader

