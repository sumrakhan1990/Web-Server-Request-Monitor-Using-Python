from flask import Flask, request, jsonify, g
import time
import monitor

app = Flask(__name__)

# Global variables to track statistics
stats = {
    "total_requests": 0,
    "average_response_time": 0.0,
    "status_codes": {},
}

@app.before_request
def before_request():
    """Log the start time of the request."""
    stats["total_requests"] += 1  # Increment request counter
    g.start_time = time.time()  # Store the request start time

@app.after_request
def after_request(response):
    """Log details of the request and response."""
    # Calculate response time
    response_time = time.time() - g.start_time
    response_time_ms = round(response_time * 1000, 2)  # Convert to milliseconds

    # Update average response time
    total_time = stats["average_response_time"] * (stats["total_requests"] - 1)
    stats["average_response_time"] = (total_time + response_time_ms) / stats["total_requests"]

    # Track status codes
    status_code = response.status_code
    stats["status_codes"][status_code] = stats["status_codes"].get(status_code, 0) + 1

    # Log details
    monitor.log_request({
        "method": request.method,
        "url": request.url,
        "status_code": status_code,
        "response_time": f"{response_time_ms} ms",
    })

    return response

@app.route('/metrics', methods=['GET'])
def metrics():
    """Endpoint to get system performance metrics."""
    performance = monitor.monitor_cpu_memory()
    return jsonify(performance)

@app.route('/stats', methods=['GET'])
def stats_endpoint():
    """Endpoint to display request statistics."""
    return jsonify(stats)


@app.route('/')
def dashboard():
    """Dashboard to display metrics graphically."""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Web Server Monitor</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(to right, #4facfe, #00f2fe);
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            header {
                background-color: #333;
                color: white;
                padding: 20px;
                width: 100%;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }
            .container {
                background: white;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 30px;
                text-align: center;
                width: 90%;
                max-width: 800px;
                margin-bottom: 30px;
            }
            canvas {
                margin-top: 20px;
                max-height: 400px;
            }
            p {
                font-size: 18px;
                color: #555;
            }
            button {
                padding: 10px 20px;
                margin: 10px;
                font-size: 16px;
                color: white;
                background-color: #007bff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #0056b3;
            }
            #rawData {
                margin-top: 20px;
                font-size: 16px;
                color: #333;
                background: #f8f9fa;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 5px;
                text-align: left;
                display: none;
            }
        </style>
    </head>
    <body>
        <header>Web Server Monitor</header>
        <div class="container">
            <h1>Request Statistics</h1>
            <canvas id="statsChart"></canvas>
            <button onclick="showStats()">Show Request Statistics</button>
        </div>
        <div class="container">
            <h1>System Metrics</h1>
            <canvas id="systemChart"></canvas>
            <button onclick="showMetrics()">Show System Metrics</button>
        </div>
        <div id="rawData"></div>
        <script>
            const statsCtx = document.getElementById('statsChart').getContext('2d');
            const systemCtx = document.getElementById('systemChart').getContext('2d');

            // Create Stats Chart
            const statsChart = new Chart(statsCtx, {
                type: 'bar',
                data: {
                    labels: ['Total Requests', 'Avg Response Time', '200 OK', '404 Not Found'], // Labels for request stats
                    datasets: [{
                        label: 'Request Statistics',
                        backgroundColor: ['#4caf50', '#ff9800', '#2196f3', '#f44336'],
                        data: [0, 0, 0, 0], // Placeholder for dynamic data
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: 'Metric' } },
                        y: { title: { display: true, text: 'Value' } }
                    }
                }
            });

            // Create System Metrics Chart
            const systemChart = new Chart(systemCtx, {
                type: 'doughnut',
                data: {
                    labels: ['CPU Usage (%)', 'Memory Usage (%)'], // Labels for system metrics
                    datasets: [{
                        label: 'System Metrics',
                        backgroundColor: ['#3e95cd', '#8e5ea2'],
                        data: [0, 0], // Placeholder for dynamic data
                    }]
                },
                options: {
                    responsive: true
                }
            });

            // Fetch Stats Data
            function fetchStats() {
                fetch('/stats')
                    .then(response => response.json())
                    .then(data => {
                        // Update stats chart
                        statsChart.data.datasets[0].data = [
                            data.total_requests, // Total Requests
                            data.average_response_time, // Avg Response Time
                            data.status_codes["200"] || 0, // 200 OK
                            data.status_codes["404"] || 0 // 404 Not Found
                        ];
                        statsChart.update(); // Refresh the chart
                    });
            }

            // Fetch System Metrics Data
            function fetchSystemMetrics() {
                fetch('/metrics')
                    .then(response => response.json())
                    .then(data => {
                        // Update system metrics chart
                        systemChart.data.datasets[0].data = [
                            data.cpu_usage, // CPU Usage
                            data.memory_usage // Memory Usage
                        ];
                        systemChart.update(); // Refresh the chart
                    });
            }

            // Show Raw Stats Data
            function showStats() {
                fetch('/stats')
                    .then(response => response.json())
                    .then(data => {
                        const rawDataDiv = document.getElementById('rawData');
                        rawDataDiv.innerHTML = `<strong>Request Statistics:</strong><pre>${JSON.stringify(data, null, 4)}</pre>`;
                        rawDataDiv.style.display = 'block';
                    });
            }

            // Show Raw Metrics Data
            function showMetrics() {
                fetch('/metrics')
                    .then(response => response.json())
                    .then(data => {
                        const rawDataDiv = document.getElementById('rawData');
                        rawDataDiv.innerHTML = `<strong>System Metrics:</strong><pre>${JSON.stringify(data, null, 4)}</pre>`;
                        rawDataDiv.style.display = 'block';
                    });
            }

            // Fetch data every 5 seconds
            setInterval(() => {
                fetchStats();
                fetchSystemMetrics();
            }, 5000);
        </script>
    </body>
    </html>
    '''
if __name__ == '__main__':
    app.run(debug=True)