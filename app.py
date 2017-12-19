import base64
import json
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from requests_futures.sessions import FuturesSession
from flask import Flask, jsonify, abort, request
from datetime import datetime

app = Flask(__name__)


@app.route('/fetch/<urls_base64>/<aggregation_strategy>')
def fetch(urls_base64, aggregation_strategy):
    urls, aggregation_strategy, error_strategy, timeout_seconds = get_verify_params(urls_base64,
                                                                                    aggregation_strategy)

    futures = []
    with FuturesSession(executor=ThreadPoolExecutor(max_workers=min(len(urls), 100))) as session:
        # fire requests as futures
        for u in urls:
            futures.append(session.get(u, timeout=timeout_seconds))

        complete_futures_or_timeout(futures, timeout_seconds)

        # collect http responses that didn't timeout or encountered an error
        http_responses = []
        for future in futures:
            http_responses.append(future.result() if future.done() else None)

        fail_fast_for_fail_any(error_strategy, http_responses)

        root_result = {} if aggregation_strategy == 'combined' else []
        for url, response in zip(urls, http_responses):
            try:
                response_body = build_url_response_body(response)
                if aggregation_strategy == 'combined':
                    root_result[url] = response_body
                else:
                    root_result.append({url: response_body})
            except:
                pass # failed to handle one response, don't give up on the rest
    return jsonify(root_result)


def fail_fast_for_fail_any(error_strategy, http_responses):
    if error_strategy == "fail_any":
        if None in http_responses: # return 500 if any of the requests timed out or exception thrown
            abort(500)
        for response in http_responses:
            response.raise_for_status() # return 500 for any responses with non 2xx code


def complete_futures_or_timeout(futures, timeout_seconds):
    started = datetime.now()
    for future in futures:
        elapsed_seconds = float((datetime.now() - started).total_seconds())
        if elapsed_seconds > timeout_seconds:
            break
        try:
            future.result(timeout=(timeout_seconds - elapsed_seconds))
        except concurrent.futures._base.TimeoutError:
            break
    print(f'elapsed_seconds={float((datetime.now() - started).total_seconds())}')


def get_verify_params(urls_base64, aggregation_strategy):
    try:
        urls_json = base64.b64decode(urls_base64).decode('utf-8')
        urls = json.loads(urls_json)
        assert len(urls) > 0
        assert aggregation_strategy in ['combined', 'appended']
        error_strategy = request.args.get('errors', 'fail_any')
        assert error_strategy in ['fail_any', 'replace']
        timeout_seconds = float(request.args.get('timeout', None)) / 1_000
        assert timeout_seconds > 0
        return urls, aggregation_strategy, error_strategy, timeout_seconds
    except:
        abort(400) # TODO: add helpful error message to client


def build_url_response_body(response):
    if response and (200 <= response.status_code < 300):
        is_json = 'application/json' in response.headers['Content-Type']
        return {
            'content': response.json() if is_json else response.text,
            'headers': dict(response.headers)
        }
    # Request raised exception, timed out, non 2xx response, or failed building response body
    return 'failed'
