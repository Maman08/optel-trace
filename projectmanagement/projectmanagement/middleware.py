import time
from django.utils.deprecation import MiddlewareMixin
from opentelemetry import metrics

class RequestMonitoringMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        meter = metrics.get_meter(__name__)
        self.request_counter = meter.create_counter(
            name="http_requests_total",
            description="Total HTTP requests"
        )
        self.request_duration = meter.create_histogram(
            name="http_request_duration_seconds",
            description="HTTP request duration in seconds",
            unit="s",
        )
        super().__init__(get_response)

    def process_request(self, request):
        request.start_time = time.time()
     

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            self.request_duration.record(
                duration,
                {
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code
                }
            )
        
        self.request_counter.add(
            1,
            {
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code
            }
        )
        
        return response 