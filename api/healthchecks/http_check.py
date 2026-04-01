import requests


def run_http_check(name, config):
    url = config.get('url')
    timeout = config.get('timeout', 10)
    expected_status = config.get('expected_status', 200)
    expected_body = config.get('expected_body')
    headers = config.get('headers', {})

    response = requests.get(url, timeout=timeout, headers=headers)
    status_ok = response.status_code == expected_status
    body_ok = True
    if expected_body is not None:
        body_ok = expected_body in response.text

    return {
        'service': name,
        'type': 'http',
        'status': 'healthy' if status_ok and body_ok else 'unhealthy',
        'response_time_ms': response.elapsed.total_seconds() * 1000,
        'status_code': response.status_code,
        'payload_ok': body_ok,
        'details': response.text[:256],
    }
