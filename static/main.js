document.getElementById('workOrderForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    fetch('/api/workorders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
    })
    .then(res => res.json())
    .then(() => {
        loadOrders();
        document.getElementById('workOrderForm').reset();
    });
});

function loadOrders() {
    fetch('/api/workorders')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('ordersContainer');
            container.innerHTML = '';
            data.forEach(order => {
                const div = document.createElement('div');
                div.className = 'order';
                div.innerHTML = `<strong>${order.title}</strong><br>${order.description}<br><em>Status: ${order.status}</em>`;
                container.appendChild(div);
            });
        });
}

loadOrders();
