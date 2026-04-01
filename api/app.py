import os
import yaml
from datetime import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models.metrics import Metric, Base as MetricBase
from models.alerts import Alert, Base as AlertBase

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///metrics.db')
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)

MetricBase.metadata.create_all(bind=engine)
AlertBase.metadata.create_all(bind=engine)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'healthchecks.yml')

@app.route('/health/status', methods=['GET'])
def health_status():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'services': [
            {'name': 'api', 'status': 'healthy'},
            {'name': 'database', 'status': 'healthy'},
            {'name': 'redis', 'status': 'healthy'},
        ],
    })

@app.route('/metrics', methods=['GET'])
def metrics():
    with SessionLocal() as session:
        metrics = session.execute(select(Metric).order_by(Metric.created_at.desc()).limit(100)).scalars().all()
        return jsonify([m.to_dict() for m in metrics])

@app.route('/metrics/history', methods=['GET'])
def metrics_history():
    service = request.args.get('service')
    with SessionLocal() as session:
        query = select(Metric)
        if service:
            query = query.where(Metric.service == service)
        query = query.order_by(Metric.created_at.desc()).limit(200)
        metrics = session.execute(query).scalars().all()
        return jsonify([m.to_dict() for m in metrics])

@app.route('/alerts', methods=['GET'])
def alerts():
    with SessionLocal() as session:
        alerts = session.execute(select(Alert).order_by(Alert.created_at.desc()).limit(50)).scalars().all()
        return jsonify([a.to_dict() for a in alerts])

@app.route('/alerts', methods=['POST'])
def create_alert():
    payload = request.json or {}
    service = payload.get('service', 'unknown')
    level = payload.get('level', 'warning')
    message = payload.get('message', 'alert triggered')
    with SessionLocal() as session:
        alert = Alert(service=service, level=level, message=message)
        session.add(alert)
        session.commit()
        return jsonify({'result': 'ok', 'id': alert.id}), 201

@app.route('/healthchecks/config', methods=['GET'])
def healthchecks_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return jsonify(config)
    except FileNotFoundError:
        return jsonify({'error': 'config not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
