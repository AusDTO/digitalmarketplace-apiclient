from __future__ import absolute_import
import logging

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import requests
from flask import has_request_context, request, current_app
import backoff
from monotonic import monotonic

import os
from functools import partial

from . import __version__
from .errors import APIError, HTTPError, HTTPTemporaryError, InvalidResponse

logger = logging.getLogger(__name__)


HTTP_VERBS = [
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'CONNECT',
    'OPTIONS',
    'TRACE',
    'PATH'
]

HTTP_VERBS_LOWER = [_.lower() for _ in HTTP_VERBS]


def make_iter_method(method_name, model_name, url_path):
    """Make a page-concatenating iterator method from a find method

    :param method_name: The name of the find method to decorate
    :param model_name: The name of the model as it appears in the JSON response
    :param url_path: The URL path for the API -- FIXME parameter ignored?
    """
    backoff_decorator = backoff.on_exception(backoff.expo, HTTPTemporaryError, max_tries=5)

    def iter_method(self, *args, **kwargs):
        method = getattr(self, method_name)
        result = backoff_decorator(method)(*args, **kwargs)
        for model in result[model_name]:
            yield model

        while True:
            if 'next' not in result['links']:
                return
            result = backoff_decorator(self._get)(result['links']['next'])
            for model in result[model_name]:
                yield model

    return iter_method


class GenericRequester(object):
    def __init__(self, client, prefix='/'):
        self.client = client
        self.prefix = prefix

    def _requester(self, *args):
        tokens = ['/'] + list(str(_) for _ in args)
        path = os.path.join(*tokens)
        path = path.lstrip(os.sep)
        prefix = os.path.join(self.prefix, path)
        return GenericRequester(self.client, prefix=prefix)

    def __getattr__(self, name):
        method_name = name

        if method_name in HTTP_VERBS_LOWER:
            method_call_name = '_{}'.format(method_name)
            method = getattr(self.client, method_call_name)
            url = self.prefix
            return partial(method, url)
        else:
            return partial(self._requester, name)


class BaseAPIClient(object):
    def __init__(self, base_url=None, auth_token=None, enabled=True):
        self.base_url = base_url
        self.auth_token = auth_token
        self.enabled = enabled
        self.req = GenericRequester(self)

    def _put(self, url, data):
        return self._request("PUT", url, data=data)

    def _put_with_updated_by(self, url, data, user):
        data = dict(data, updated_by=user)
        return self._put(url, data)

    def _get(self, url, params=None, data=None):
        return self._request("GET", url, params=params, data=data)

    def _post(self, url, data):
        return self._request("POST", url, data=data)

    def _patch(self, url, data):
        return self._request("PATCH", url, data=data)

    def _post_with_updated_by(self, url, data, user):
        data = dict(data, updated_by=user)
        return self._post(url, data)

    def _delete(self, url, data=None):
        return self._request("DELETE", url, data=data)

    def _delete_with_updated_by(self, url, data, user):
        data = dict(data, updated_by=user)
        return self._delete(url, data)

    def _request(self, method, url, data=None, params=None):
        if not self.enabled:
            return None

        url = url.lstrip('/')
        url = urlparse.urljoin(self.base_url, url)

        logger.debug("API request {method} {url}",
                     extra={
                         'method': method,
                         'url': url
                     })
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer {}".format(self.auth_token),
            "User-agent": "DM-API-Client/{}".format(__version__),
        }
        headers = self._add_request_id_header(headers)
        headers = self._add_zipkin_tracing_headers(headers)

        start_time = monotonic()
        try:
            response = requests.request(
                method, url,
                headers=headers, json=data, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            api_error = HTTPError.create(e)
            elapsed_time = monotonic() - start_time
            logger.log(
                logging.INFO if api_error.status_code == 404 else logging.WARNING,
                "API {api_method} request on {api_url} failed with {api_status} '{api_error}'",
                extra={
                    'api_method': method,
                    'api_url': url,
                    'api_status': api_error.status_code,
                    'api_error': api_error.message,
                    'api_time': elapsed_time
                })
            raise api_error
        else:
            elapsed_time = monotonic() - start_time
            logger.info(
                "API {api_method} request on {api_url} finished in {api_time}",
                extra={
                    'api_method': method,
                    'api_url': url,
                    'api_status': response.status_code,
                    'api_time': elapsed_time
                })
        try:
            return response.json()
        except ValueError as e:
            raise InvalidResponse(response,
                                  message="No JSON object could be decoded")

    def _add_request_id_header(self, headers):
        if not has_request_context():
            return headers
        if 'DM_REQUEST_ID_HEADER' not in current_app.config:
            return headers
        header = current_app.config['DM_REQUEST_ID_HEADER']
        headers[header] = request.request_id
        return headers

    def _add_zipkin_tracing_headers(self, headers):
        if not has_request_context():
            return headers

        span_id = request.headers.get('X-B3-SpanId', None)
        trace_id = request.headers.get('X-B3-TraceId', None)

        if span_id:
            headers['X-B3-SpanId'] = span_id

        if trace_id:
            headers['X-B3-TraceId'] = trace_id

        return headers

    def get_status(self):
        try:
            return self._get("{}/_status".format(self.base_url))
        except APIError as e:
            try:
                return e.response.json()
            except (ValueError, AttributeError):
                return {
                    "status": "error",
                    "message": "{}".format(e.message),
                }
