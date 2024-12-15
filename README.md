# Web Server Request Monitor  

A real-time monitoring system designed to track server performance, analyze HTTP requests, and assist administrators in ensuring smooth server operations.  

---

## 📋 Overview  

The **Web Server Request Monitor** helps server administrators maintain optimal performance by monitoring key metrics such as:  
- **CPU and Memory Usage**  
- **Total Requests**  
- **Average Response Time**  
- **HTTP Status Codes**  

It includes an intuitive dashboard for performance visualization and detailed analysis of server activity.  

---

## 🚀 Features  

### 📊 **System Performance Monitoring**  
- Tracks **CPU** and **memory usage** in real-time using the `psutil` library.  

### 🔍 **Request Tracking**  
- Logs every HTTP request with details:  
  - Request Method and URL  
  - Status Code  
  - Response Time  

### 📈 **Real-Time Metrics**  
- Provides aggregated data:  
  - Total Requests  
  - Average Response Time  
  - Status Code Counts  

### 🖥 **Interactive Dashboard**  
- Displays server health and offers links to JSON endpoints for detailed statistics.  

---

## 🛠 Methodology  

1. **Initialization**  
   - Flask server initializes, preparing to track performance metrics.  
2. **Request Handling**  
   - Logs requests, updates performance metrics, and processes responses.  
3. **Data Display**  
   - JSON Endpoints: Accessible at `/metrics` and `/stats`.  
   - Dashboard: Accessible at `/` for server health visualization.  

---

## ⚙️ Technology Stack  

- **Programming Language**: Python  
- **Framework**: Flask  
- **Core Libraries**:  
  - `psutil`: System monitoring  
  - `os`, `time`: Utility functions  
- **Dashboard**: HTML interface for visualization  

---

## 📄 Example Outputs  

### Logs (`monitor_logs.txt`)  
```plaintext  
2024-11-22 10:00:00 - CPU Usage: 25.5%, Memory Usage: 50.2%  
2024-11-22 10:01:00 - Request: Method=GET, URL=/metrics, Status=200, Response Time=120ms  
```  

### JSON Responses  
**Endpoint: `/metrics`**  
```json  
{
  "cpu_usage": 23.5,
  "memory_usage": 55.8
}
```  

**Endpoint: `/stats`**  
```json  
{
  "total_requests": 5,
  "average_response_time": 120.5,
  "status_codes": {
    "200": 4,
    "404": 1
  }
}
```  

---

## 🔮 Future Scope  

- **Expanded Metrics**: Add disk usage, network activity, and I/O stats.  
- **Multi-Server Support**: Monitor multiple servers simultaneously.  
- **Alerts and Notifications**: Integrate warnings for high resource usage or frequent errors.  
- **Advanced Analytics**: Incorporate machine learning for predicting bottlenecks.  

---

## 🏁 Conclusion  

The **Web Server Request Monitor** simplifies server management by providing real-time insights into server health and performance. With Python, Flask, and `psutil`, it offers a scalable and user-friendly solution for modern server environments.  
