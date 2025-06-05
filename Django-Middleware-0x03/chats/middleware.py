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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        restricted_path = '/chats/'

        # Block access if not between 18 (6PM) and 21 (9PM)
        if request.path.startswith(restricted_path) and not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chats is only allowed between 6PM and 9PM.")

        return self.get_response(request)