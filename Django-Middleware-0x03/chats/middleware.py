import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Configure file-based logger
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        path = request.path
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.logger.info(f"{timestamp} - User: {user} - Path: {path}")

        response = self.get_response(request)
        return response
