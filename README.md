# Merchant Payment Gateway System

A production-ready, full-stack payment gateway solution featuring a Merchant Dashboard and a Hosted Checkout experience. This project demonstrates the complete lifecycle of a payment, from order creation to transaction settlement.

## 🌟 Core Features

### 1. Merchant Dashboard (Port 3000)
- **Authentication**: Secure login using pre-seeded test credentials.
- **Analytics Overview**: Real-time display of Total Revenue (in Rupees), Successful Payments, and Failed Payments.
- **Order Management**: Create orders with a unique `order_` prefix and track status history.
- **Transaction Monitoring**: A detailed table displaying Payment IDs, Order IDs, and raw amounts in Paise for automated audit compliance.

### 2. Hosted Checkout (Port 3001)
- **Selection Interface**: Option to choose between UPI and Card payment methods.
- **Processing Engine**: Simulated payment processing with a visual loading state.
- **Success/Failure Handling**: Dedicated views for payment outcomes, including a "Finish & Return" feature that automatically synchronizes with the original Dashboard tab and closes the checkout tab.

### 3. Backend API (Port 8000)
- **FastAPI Core**: High-performance RESTful API.
- **Merchant Security**: Header-based authentication using `X-Api-Key` and `X-Api-Secret`.
- **Persistence**: Relational database storage using PostgreSQL.

---

## 🏗️ System Architecture
![Architecture Diagram](./docs/architecture_diagram.png)

## 🚀 Quick Start (Docker)

The system is fully containerized using Docker Compose. Ensure Docker is running on your machine before starting.

1. **Clone the repository:**
```bash 
git clone https://github.com/Ramesh-Tatapudi2005/payment-gateway-merchant-system.git
cd payment-gateway-merchant-system
```

2. **Build and Start Services**:
   ```bash
   docker-compose up --build
   ```

3. **Access applications**:
- **Dashboard**: http://localhost:3000
- **Checkout** : http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)** : http://localhost:8000/docs

## 📡 API Interaction Flow

To maintain security, the system splits the payment lifecycle into two distinct permission zones:

| Flow Phase | Endpoint | Auth Required | Responsibility |
| :--- | :--- | :--- | :--- |
| **Order Creation** | `POST /api/v1/orders` | **Private** (`X-Api-Secret`) | Merchant Server |
| **Public Info** | `GET /api/v1/orders/{id}/public` | **Public** (None) | Checkout UI |
| **Payment Init** | `POST /api/v1/payments/public` | **Public** (None) | Checkout UI |
| **Status Polling** | `GET /api/v1/payments/{id}/public` | **Public** (None) | Checkout UI |
| **Audit Logs** | `GET /api/v1/payments` | **Private** (`X-Api-Secret`) | Merchant Dashboard |

## 🔑 Login Credentials
Use these credentials to evaluate the merchant authentication and API security:

- **Login Email** : test@example.com
- **Password** : password123

## API Authentication (Headers)
- **Test API Key** : key_test_abc123
- **Test API Secret** : secret_test_xyz789

## ✅ Key Requirements Satisfied
1. **Asynchronous State Machine (Bank Latency Simulation)**
   - **Requirement**: Payments must enter a `processing` state before moving to `success` or `failed`.
   - **Implementation**: The system commits a record to the database **before** triggering the simulated bank delay (5-10s). This allows frontend polling services to retrieve a "Processing" status immediately, matching real-world gateway behavior.
   - **Uniform Delay**: Even invalid card attempts (Luhn failures) are subjected to the processing delay, preventing "instant rejection" and ensuring the system remains resilient against timing attacks.

2. **Advanced Card Validation & IIN Detection**
   - **Luhn Check**: Uses a Mod-10 Checksum to validate card numbers server-side.
   - **IIN Detection**: Identifies card networks (Visa, Mastercard, RuPay) dynamically during the processing phase and persists the network type to the audit log.
   - **Masking Compliance**: Only the `card_last4` and `card_network` are stored in the database; full card numbers are processed entirely in-memory and never persisted.

3. **Public vs. Private Endpoints (Security)**
To prevent the leakage of Merchant Secrets:
- **Private Routes**:`X-Api-Key` and `X-Api-Secret`. Used for order generation.
- **Public Routes** :No credentials required. Used by the Checkout Page to fetch basic order info and process payments without exposing merchant keys to the browser.

4. **Deterministic Test Mode**
Supports `TEST_MODE=true` in `.env` for automated evaluation, allowing for predictable successes, failures, and processing delays.

## 📁 Project Structure

The project is organized into three main service directories and a centralized orchestration configuration:

```text
PAYMENT-GATEWAY/
├── backend/                # FastAPI Application Service
│   ├── app/                # Application logic (Models, Routes, Schemas)
│   ├── Dockerfile          # Container definition for the API
│   └── requirements.txt    # Python dependencies
├── checkout-page/          # Hosted Checkout Interface Service
│   ├── public/             # Static assets
│   ├── src/                # React source code (Success, Failure, Checkout)
│   ├── Dockerfile          # Container definition for the Checkout UI
│   ├── nginx.conf          # Nginx configuration for production serving
│   └── package.json        # Frontend dependencies
├── frontend/               # Merchant Dashboard Service
│   ├── node_modules/       # Local dependencies (Ignored in Git)
│   ├── public/             # Static assets
│   ├── src/                # React source code (Dashboard, Sidebar, etc.)
│   ├── Dockerfile          # Container definition for the Dashboard UI
│   ├── package-lock.json   
│   └── package.json        # Frontend dependencies
├── .env                    # Root environment variables (API keys/secrets)
├── .gitignore              # Git exclusion rules
├── docker-compose.yml      # Multi-container orchestration
└── README.md               # Project documentation
```

## ✅ Automated Evaluation Compliance
- **Test IDs** : Every critical UI element (Success Message, Payment ID, Error State, etc.) is tagged with the mandatory `data-test-id` attributes.
- **Unit Precision** : The transaction table displays amounts in the smallest currency unit (Paise) as required for automated testing.
- **State Persistence** : Success and Failure pages implement the window.opener protocol to refresh the Merchant Dashboard upon completion.

## 📡 API Interaction Flow

To maintain security, the system splits the payment lifecycle into two distinct permission zones:

| Flow Phase | Endpoint | Auth Required | Responsibility |
| :--- | :--- | :--- | :--- |
| **Order Creation** | `POST /api/v1/orders` | **Private** (`X-Api-Secret`) | Merchant Server |
| **Public Info** | `GET /api/v1/orders/{id}/public` | **Public** (None) | Checkout UI |
| **Payment Init** | `POST /api/v1/payments/public` | **Public** (None) | Checkout UI |
| **Status Polling** | `GET /api/v1/payments/{id}/public` | **Public** (None) | Checkout UI |
| **Audit Logs** | `GET /api/v1/payments` | **Private** (`X-Api-Secret`) | Merchant Dashboard |

## 🎥 Documentation Artifacts
- **Postman Collection** : `/docs/payment_gateway.postman_collection.json`.


## 🧪 Automated Testing Support

This project is built to be compatible with automated evaluation suites.
- **Test IDs**: High-traffic elements like `success-state`, `payment-id`, and `error-message` use specific `data-test-id` attributes for reliable selection.
- **Data Precision**: All currency amounts in the transaction tables are rendered as raw integers (Paise) to match backend audit logs.
- **Cross-Tab Communication**: The system uses `window.opener` and `postMessage` to ensure the Merchant Dashboard stays synchronized with the Hosted Checkout status without manual refreshes.

## 🛠️ Local Development & Debugging

If you need to run services outside of Docker for debugging:

1. **Backend**:
   - Navigate to `/backend`
   - Run `pip install -r requirements.txt`
   - Start server: `uvicorn app.main:app --reload --port 8000`
2. **Dashboard**:
   - Navigate to `/frontend`
   - Run `npm install && npm start` (Runs on Port 3000)
3. **Checkout**:
   - Navigate to `/checkout-page`
   - Run `npm install && npm start` (Runs on Port 3001)

## 🏁 Submission Notes
- **Deadline Compliance**: This version represents the final submission for the 5 PM deadline.
- **Seeded Data**: Upon first launch, the system is pre-configured with the required merchant profile and test API credentials.

---
**Technical Submission Checklist:**
- [x] Docker-compose healthchecks implemented for backend dependency.
- [x] Trailing slash redirection handled in FastAPI routers.
- [x] Database record created *prior* to `time.sleep` (State Machine compliance).
- [x] `PYTHONPATH` configured in Dockerfile for module discovery.