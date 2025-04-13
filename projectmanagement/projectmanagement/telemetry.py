from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor


def setup_telemetry():
    # Setup tracing
    resource = Resource.create({"service.name": "projectmanagement"})
    trace.set_tracer_provider(TracerProvider(resource=resource))

    # Setup metrics
    prometheus_reader = PrometheusMetricReader()
    metric_readers = [prometheus_reader]
    meter_provider = MeterProvider(metric_readers=metric_readers, resource=resource)

    # Instrumentations
    DjangoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    MySQLInstrumentor().instrument()

    return prometheus_reader
