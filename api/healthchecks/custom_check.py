import socket


def run_custom_check(name, config):
    if config.get('type') == 'tcp':
        host = config.get('host')
        port = int(config.get('port', 0))
        timeout = config.get('timeout', 5)

        try:
            with socket.create_connection((host, port), timeout=timeout):
                return {
                    'service': name,
                    'type': 'tcp',
                    'status': 'healthy',
                    'host': host,
                    'port': port,
                }
        except Exception as exc:
            return {
                'service': name,
                'type': 'tcp',
                'status': 'unhealthy',
                'error': str(exc),
            }

    return {
        'service': name,
        'type': 'custom',
        'status': 'unknown',
        'error': 'unsupported custom check',
    }
