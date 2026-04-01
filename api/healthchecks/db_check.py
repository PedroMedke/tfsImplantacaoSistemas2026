from sqlalchemy import create_engine, text


def run_db_check(name, config):
    connection = config.get('connection')
    query = config.get('query', 'SELECT 1')
    timeout = config.get('timeout', 30)

    engine = create_engine(connection, connect_args={'connect_timeout': timeout}, future=True)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            value = result.scalar()
            status = 'healthy' if value is not None else 'unhealthy'
            return {
                'service': name,
                'type': 'database',
                'status': status,
                'response_time_ms': None,
                'database_value': value,
            }
    except Exception as exc:
        return {
            'service': name,
            'type': 'database',
            'status': 'unhealthy',
            'error': str(exc),
        }
