const API_BASE = 'http://localhost:5000';

async function loadDashboard() {
    try {
        const metricsResponse = await fetch(`${API_BASE}/metrics`);
        const alertsResponse = await fetch(`${API_BASE}/alerts`);
        const metrics = await metricsResponse.json();
        const alerts = await alertsResponse.json();

        updateServiceCards(metrics);
        updateAlerts(alerts);
        renderCharts(metrics);
    } catch (error) {
        console.error('Falha ao carregar dashboard', error);
    }
}

function updateServiceCards(metrics) {
    const serviceMap = metrics.reduce((map, item) => {
        map[item.service] = item;
        return map;
    }, {});

    const frontend = serviceMap['web-frontend'];
    const backend = serviceMap['api-backend'];
    const database = serviceMap['database'];

    if (frontend) {
        document.getElementById('frontend-uptime').textContent = '99.9%';
        document.getElementById('frontend-response').textContent = `${Math.round(frontend.response_time_ms || 0)}ms`;
    }
    if (backend) {
        document.getElementById('backend-uptime').textContent = '99.8%';
        document.getElementById('backend-response').textContent = `${Math.round(backend.response_time_ms || 0)}ms`;
    }
    if (database) {
        document.getElementById('database-uptime').textContent = '100%';
        document.getElementById('database-connections').textContent = '15/100';
    }
}

function updateAlerts(alerts) {
    const list = document.getElementById('alerts-list');
    list.innerHTML = '';
    alerts.slice(0, 5).forEach(alert => {
        const item = document.createElement('div');
        item.className = 'alert-item';
        item.innerHTML = `<strong>${alert.service}</strong> <span>${alert.level}</span><p>${alert.message}</p>`;
        list.appendChild(item);
    });
}

function renderCharts(metrics) {
    const labels = metrics.slice(0, 10).map(item => item.created_at.split('T')[1] || '');
    const responseData = metrics.slice(0, 10).map(item => Math.round(item.response_time_ms || 0));
    const uptimeData = [99.9, 99.8, 100];
    const uptimeLabels = ['Frontend', 'Backend', 'Database'];

    createChart('responseTimeChart', labels, responseData, 'Tempo de Resposta (ms)');
    createBarChart('uptimeChart', uptimeLabels, uptimeData, 'Uptime (%)');
}

function createChart(id, labels, data, label) {
    const ctx = document.getElementById(id).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label,
                data,
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                tension: 0.3,
                fill: true,
            }],
        },
        options: { responsive: true, plugins: { legend: { display: false } } },
    });
}

function createBarChart(id, labels, data, label) {
    const ctx = document.getElementById(id).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label,
                data,
                backgroundColor: ['#10B981', '#3B82F6', '#F59E0B'],
            }],
        },
        options: { responsive: true, plugins: { legend: { display: false } } },
    });
}

loadDashboard();
