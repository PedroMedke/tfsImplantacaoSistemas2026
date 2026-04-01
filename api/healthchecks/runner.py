import argparse
import os
import sys
import time
import yaml
import json
import requests
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models.metrics import Metric, Base as MetricBase
from models.alerts import Alert, Base as AlertBase
from http_check import run_http_check
from db_check import run_db_check
from custom_check import run_custom_check

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
HEALTHCHECKS_FILE = os.path.join(CONFIG_DIR, 'healthchecks.yml')
ALERTS_FILE = os.path.join(CONFIG_DIR, 'alerts.yml')
DEFAULT_DB_URL = os.environ.get('DATABASE_URL', 'sqlite:///metrics.db')

engine = create_engine(DEFAULT_DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
MetricBase.metadata.create_all(bind=engine)
AlertBase.metadata.create_all(bind=engine)


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def send_alert(alert_payload):
    alerts_config = load_yaml(ALERTS_FILE).get('alerts', {})
    webhook = alerts_config.get('webhook', {})
    if webhook.get('enabled') and webhook.get('url'):
        try:
            requests.post(webhook['url'], json=alert_payload, timeout=5)
        except Exception:
            pass


def create_alert(service, level, message):
    with SessionLocal() as session:
        alert = Alert(service=service, level=level, message=message)
        session.add(alert)
        session.commit()
    send_alert({'service': service, 'level': level, 'message': message})


def save_metric(check):
    with SessionLocal() as session:
        metric = Metric(
            service=check.get('service', 'unknown'),
            status=check.get('status', 'unknown'),
            response_time_ms=check.get('response_time_ms'),
            error_rate=0.0,
        )
        session.add(metric)
        session.commit()


def run_check(name, definition):
    check_type = definition.get('type')
    if check_type == 'http':
        return run_http_check(name, definition)
    if check_type == 'database':
        return run_db_check(name, definition)
    if check_type in ('tcp', 'custom'):
        return run_custom_check(name, definition)
    return {'service': name, 'status': 'unknown', 'error': 'unsupported healthcheck type'}


def evaluate(result):
    if result.get('status') != 'healthy':
        create_alert(result['service'], 'critical', json.dumps(result, default=str))
        return False
    return True


def print_summary(results):
    for item in results:
        status = item.get('status')
        print(f"{item.get('service')}: {status}")
        if item.get('response_time_ms') is not None:
            print(f"  response_time_ms: {item['response_time_ms']:.1f}")
    healthy_count = sum(1 for item in results if item.get('status') == 'healthy')
    print(f"Summary: {healthy_count}/{len(results)} healthy")


def run_all_checks(selected=None, watch=False):
    config = load_yaml(HEALTHCHECKS_FILE).get('healthchecks', {})
    services = [selected] if selected else list(config.keys())
    while True:
        results = []
        for name in services:
            if name not in config:
                continue
            result = run_check(name, config[name])
            save_metric(result)
            evaluate(result)
            results.append(result)
        print_summary(results)
        if not watch:
            break
        time.sleep(10)


def report():
    with SessionLocal() as session:
        metrics = session.execute(select(Metric).order_by(Metric.created_at.desc()).limit(10)).scalars().all()
        for metric in metrics:
            print(f"[{metric.created_at}] {metric.service} = {metric.status} ({metric.response_time_ms})")


def test_alerts():
    create_alert('health-monitor', 'warning', 'Teste de alerta disparado com sucesso')
    print('Alerta de teste criado e enviado via webhook, se configurado.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Healthcheck runner')
    parser.add_argument('--pre-deploy', action='store_true')
    parser.add_argument('--check', type=str)
    parser.add_argument('--check-all', action='store_true')
    parser.add_argument('--watch', action='store_true')
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--test-alerts', action='store_true')
    args = parser.parse_args()

    if args.pre_deploy or args.check_all:
        run_all_checks(watch=False)
    elif args.check:
        run_all_checks(selected=args.check, watch=False)
    elif args.watch:
        run_all_checks(watch=True)
    elif args.report:
        report()
    elif args.test_alerts:
        test_alerts()
    else:
        parser.print_help()
