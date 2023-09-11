from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from typing import Callable
import logging
from django.utils.deprecation import MiddlewareMixin

import socket
import time
import json
import pymongo


UserModel = get_user_model()

request_logger = logging.getLogger('django.request')

mongoclient = pymongo.MongoClient("mongodb://46.101.106.224:27017/")
avtobaza_db = mongoclient["Logs"] # set database

request_logs = avtobaza_db["request_logs"] # set collections


class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware."""

    def __init__(self, *args, **kwargs):
            """Constructor method."""
            super().__init__(*args, **kwargs)

    def process_request(self, request):
        """Set Request Start Time to measure time taken to service request."""
        if request.method in ['POST', 'PUT', 'PATCH']:
            request.req_body = request.body
        if str(request.get_full_path()).startswith('/'):
            request.start_time = time.time()

    def extract_log_info(self, request, response=None, exception=None):
        """Extract appropriate log info from requests/responses/exceptions."""
        try:
            log_data = {
                'remote_address': request.META['REMOTE_ADDR'],
                'server_hostname': socket.gethostname(),
                'request_method': request.method,
                'request_path': request.get_full_path(),
                'ip_address': request.META.get('REMOTE_ADDR'),
                'run_time': time.time() - request.start_time,
            }
            if request.method in ['PUT', 'POST', 'PATCH']:
                try:
                    log_data['request_body'] = json.loads(
                    str(request.req_body, 'utf-8'))
                except:
                    log_data['request_body'] = json.loads(
                    str(request.req_body))
                if response:
                    response_body = response.content
                    log_data['response_body'] = response_body
            log = request_logs.insert_one(log_data)
            return log_data
        except json.JSONDecodeError:
            return None

    def process_response(self, request, response):
        """Log data using logger."""
        if str(request.get_full_path()).startswith('/'):
                log_data = self.extract_log_info(request=request,
                                                 response=response)
                request_logger.debug(msg='', extra=log_data)
        return response

    def process_exception(self, request, exception):
        """Log Exceptions."""
        try:
            raise exception
        except Exception:
            request_logger.exception(msg="Unhandled Exception")
        return exception


class BlacklistMiddleware:
    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self.handle_request(request)
        response = self.get_response(request)
        self.handle_response(response)

        return response

    def handle_request(self, request: HttpRequest) -> None:
        user__login_auth0 = request.session.get("user")
        if not user__login_auth0:
            return

        blacklist, _ = Group.objects.get_or_create(name="Blacklist")

        if blacklist.user_set.filter(email=user__login_auth0["userinfo"]["nickname"]).exists():
            raise PermissionDenied()

    def handle_response(self, response: HttpResponse) -> None:
        ...