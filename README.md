# MDC Logger

## 📖 Overview
`mdc_trace_logger` is a lightweight Python logging library that provides **Mapped Diagnostic Context (MDC)** support for multi-threaded applications. It formats logs in **ECS (Elastic Common Schema)** format, making it easy to integrate with logging systems like **Elasticsearch, Kibana, and Logstash**.

## 🚀 Why Use `mdc_trace_logger`?
### 🔥 **Powerful Logging with Context**
Traditional logging does not maintain context across different parts of an application. With `mdc_trace_logger`, you can enrich logs with **user details, request IDs, session information**, and any other metadata.

### 🌍 **Seamless Multi-Threading**
`mdc_trace_logger` ensures **each thread retains its own logging context**, preventing data leakage between concurrent tasks.

### 🛠 **ECS-Compliant Structured Logs**
Your logs will automatically be formatted to **Elastic Common Schema (ECS)**, making it easier to analyze and visualize data in Kibana and other log monitoring tools.

### 🔗 **Works with Flask, FastAPI, and Any Python App**
With built-in middleware support, `mdc_trace_logger` can **inject context into logs automatically**, making debugging and tracing effortless.

### ⚡ **Easy to Configure with YAML**
No need for complex setup. Just drop a YAML config file, and you’re ready to go!

### 🎯 **Hook System for Custom Actions**
A unique feature of `mdc_trace_logger` is its **hook system**, allowing developers to execute custom logic every time the MDC context updates. This is great for **real-time monitoring, performance tracking, or external logging integrations**.

---

## 📌 Installation
Install the library via **pip**:

```sh
pip install mdc_trace_logger
```

---

## 📌 Basic Usage

Here's a simple example of how to use `mdc_trace_logger`:

```python
from mdc_trace_logger import MDC, get_logger

logger = get_logger(__name__)

with MDC(user="test_user", request_id="123456"):
    logger.info("User made a request.")

logger.info("This log will NOT have MDC data.")
```

---

## 🎯 Using Hooks in `mdc_trace_logger`
Hooks allow you to execute **custom functions** whenever MDC data is updated. This is useful for tracking analytics, sending alerts, or modifying logs dynamically.

### **Registering a Hook**
```python
from mdc_trace_logger import MDC

def my_custom_hook(mdc_data):
    print("Hook triggered with MDC data:", mdc_data)

MDC.register_hook(my_custom_hook)

with MDC(user="admin", session_id="xyz123"):
    pass  # Hook will be executed here
```
📌 **Expected Output:**
```
Hook triggered with MDC data: {'user': 'admin', 'session_id': 'xyz123'}
```

---

## 🏗️ Using `mdc_trace_logger` in Flask (as Middleware)

You can automatically inject MDC data (like `request_id` and `user`) into your logs using **Flask Middleware**:

```python
from flask import Flask, request
from mdc_trace_logger import MDC, get_logger

app = Flask(__name__)
logger = get_logger(__name__)

@app.before_request
def add_mdc_context():
    MDC.set_global_context({
        "request_id": request.headers.get("X-Request-ID", "unknown"),
        "user": request.headers.get("X-User", "anonymous")
    })

@app.route("/")
def index():
    logger.info("Handling request")
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## ⚡ Using `mdc_trace_logger` in FastAPI (as Middleware)

For **FastAPI**, you can use a middleware to inject MDC data before each request:

```python
from fastapi import FastAPI, Request
from mdc_trace_logger import MDC, get_logger

app = FastAPI()
logger = get_logger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    MDC.set_global_context({
        "request_id": request.headers.get("X-Request-ID", "unknown"),
        "user": request.headers.get("X-User", "anonymous")
    })
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    logger.info("Received request")
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🛠️ Using Configuration Files

You can control logging behavior using a **YAML configuration file**.

### **1️⃣ Create a config file** (e.g., `production.logger.config.yaml`):
```yaml
logger_name: "my_application"
log_level: "INFO"
log_to_console: true
log_to_file: true
log_file: "logs/app.log"
use_ecs_format: true
log_level_upper: true
```

### **2️⃣ Set environment variables**:
```sh
export MDC_ENVIRONMENT=production
export mdc_trace_logger_CONFIG=production.logger.config.yaml
```

### **3️⃣ Load config in your application**:
```python
from mdc_trace_logger import CONFIG, get_logger

logger = get_logger()
logger.info("Application started!")
```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🏆 Contributing
Pull requests are welcome! Feel free to open an issue if you find a bug or have a feature request.

---

## 🔗 Links
- **PyPI**: [https://pypi.org/project/mdc_trace_logger/](https://pypi.org/project/mdc_trace_logger/)
- **GitHub**: [https://github.com/Bulga-xD/mdc_trace_logger](https://github.com/Bulga-xD/mdc-trace-logger)
