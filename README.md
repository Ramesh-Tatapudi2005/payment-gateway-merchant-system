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

## 🚀 Live Demo & Evaluation Guide

The system is fully deployed across three services on Render. Follow these steps to evaluate the complete payment lifecycle in real-time.

### 🔗 Live Service Entry Points
* **Merchant Dashboard:** [https://merchant-dashboard-ui.onrender.com](https://merchant-dashboard-ui.onrender.com)
* **Hosted Checkout:** [https://checkout-page-ui.onrender.com](https://checkout-page-ui.onrender.com)
* **API Documentation:** [https://gateway-api-service.onrender.com/docs](https://gateway-api-service.onrender.com/docs)

### 🔑 Test Credentials
Use these pre-seeded credentials to explore the system:
| Credential | Value |
| :--- | :--- |
| **Merchant Email** | `test@example.com` |
| **password** | `password123` |
| **Merchant API Key** | `key_test_abc123` |
| **Merchant API Secret** | `secret_test_xyz789` |

---

### 🧪 Step-by-Step Evaluation Process

#### 1. System Health Verification
Verify that the Backend and PostgreSQL database are online:
- Open the [Health Endpoint](https://gateway-api-service.onrender.com/health).
- Confirm the JSON response shows: `"database": "connected"`.

#### 2. Merchant Dashboard Login
- Navigate to the **Merchant Dashboard**.
- Log in using `test@example.com` and `key_test_abc123` and `password123`.
- Observe the real-time analytics for the "Test Merchant."

#### 3. Create an Order
- Click **"Create Order"** in the sidebar.
- Enter an amount (e.g., `500.00`) and a description.
- Submit to see the order appear in the "Recent Orders" table with a `PENDING` status.

#### 4. Complete the Payment Flow
- Click the **"Pay Now"** button next to your order. This opens the **Hosted Checkout** in a new tab.
- Select **Card** or **UPI**.
- Enter payment details and click **"Pay"**. 
- Wait for the simulated **Bank Latency** (approx. 5-7 seconds) to move from "Processing" to "Success."
- Click **"Finish & Return"**. The tab will close, and the Dashboard will auto-refresh.

#### 5. Verify the Audit Trail
- Observe the **Transaction Table** on the Dashboard.
- Verify the **Payment ID** is generated and the amount is correctly logged in **Paise** for accounting precision.

--- 

### 🛠️ Manual API Testing (Live Evaluation)

The backend logic is hosted live on Render and can be tested using tools like **Postman**, **cURL**, or the **interactive documentation**. No local setup or repository cloning is required to verify the API's functionality.

> **Base URL**: `https://gateway-api-service.onrender.com`

| Action | Method | Full Live URL | Auth Required |
| :--- | :--- | :--- | :--- |
| **System Health** | `GET` | `https://gateway-api-service.onrender.com/health` | None |
| **Merchant Login** | `POST` | `https://gateway-api-service.onrender.com/api/v1/auth/login` | None |
| **Create Order** | `POST` | `https://gateway-api-service.onrender.com/api/v1/orders` | `X-Api-Key` & `X-Api-Secret` |
| **List Payments** | `GET` | `https://gateway-api-service.onrender.com/api/v1/payments` | `X-Api-Key` & `X-Api-Secret` |

---

#### 📦 Sample Request Bodies & Commands

**1. System Health Check**
*Can be tested directly in your browser address bar.*
- **URL**: `https://gateway-api-service.onrender.com/health`
- **Expected Response**: `{"status": "healthy", "database": "connected"}`

**2. Create Order (Private Merchant API)**
*Requires headers. Use Postman or cURL.*
- **URL**: `https://gateway-api-service.onrender.com/api/v1/orders`
- **Headers**: 
  - `X-Api-Key: key_test_abc123`
  - `X-Api-Secret: secret_test_xyz789`
- **JSON Body**:
```json
{
  "amount": 250.75,
  "currency": "INR",
  "description": "Evaluator Test Transaction"
}
```
3. **Process Public Payment**  
Note: Use an order_id generated from the step above.  
- **URL** : `https://gateway-api-service.onrender.com/api/v1/payments/public`  
- **JSON Body:**  
```json
{
  "order_id": "PASTE_ORDER_ID_HERE",
  "payment_method": "card",
  "card_info": {
    "card_number": "4111111111111111",
    "expiry_date": "12/28",
    "cvv": "123"
  }
}
```  
## 🧪 Direct Browser Testing (Swagger UI)  
For the most convenient testing experience, use the interactive documentation:  
1. Navigate to: `https://gateway-api-service.onrender.com/docs`  
2. Select an endpoint and click **"Try it out"**.  
3. Fill in the parameters and click **"Execute"** to see the live response from the database.


### 🖥️ Local Environment (Docker)  

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
- **API Docs (Swagger)** : http://localhost:8000/docs (Recommended for checking the APIs)

## 📡 API Interaction Flow (Postman)

| Flow Phase | Endpoint | Auth Required | Responsibility |
| :--- | :--- | :--- | :--- |
| **Order Creation** | `POST /api/v1/orders` | **Private** (`X-Api-Secret`) | Merchant Server |
| **Public Info** | `GET /api/v1/orders/{id}/public` | **Public** (None) | Checkout UI |
| **Payment Init** | `POST /api/v1/payments/public` | **Public** (None) | Checkout UI |
| **Status Polling** | `GET /api/v1/payments/{id}/public` | **Public** (None) | Checkout UI |
| **Audit Logs** | `GET /api/v1/payments` | **Private** (`X-Api-Secret`) | Merchant Dashboard |


## API Authentication (Headers)
- **Test API Key** : key_test_abc123
- **Test API Secret** : secret_test_xyz789


## 🏗️ System Architecture
![Architecture Diagram](./docs/architecture_diagram.png)  

## 🛡️ Security & Compliance Implementation

This project is designed with a "Security-First" approach, mimicking real-world payment gateway standards to ensure data integrity and credential safety.

### 1. API Authentication & Authorization
- **Header-Based Security**: Private endpoints (like Order Creation and Audit Logs) strictly enforce `X-Api-Key` and `X-Api-Secret` validation.
- **Credential Isolation**: The system uses a **Dual-Zone** security model:
    - **Private Zone**: Requires full secrets for server-to-server communication.
    - **Public Zone**: Uses only temporary IDs (like `order_id`) for the Checkout UI, ensuring that merchant secrets are **never** exposed to the customer's browser or frontend logs.

### 2. PCI-DSS Principles (Card Data Handling)
- **Zero-Persistence Policy**: Full Primary Account Numbers (PAN) and CVVs are processed entirely in-memory for validation and are **never** stored in the database.
- **Data Masking**: Only non-sensitive metadata is persisted for audit purposes:
    - `card_last4`: The last four digits of the card.
    - `card_network`: Identified dynamically (Visa, Mastercard, RuPay, etc.).
- **Server-Side Validation**: All card data is validated using the **Luhn Algorithm (Mod-10 Checksum)** server-side to prevent fraudulent processing attempts.

### 3. Transaction Integrity (State Machine)
- **Atomic Transitions**: Payment statuses follow a deterministic state machine: `PENDING` ➔ `PROCESSING` ➔ `SUCCESS` / `FAILED`.
- **Latency Resilience**: The system commits transaction records to the PostgreSQL database **before** the simulated bank delay, ensuring that state is preserved even if a network timeout occurs during the processing phase.
- **CORS Protection**: Cross-Origin Resource Sharing (CORS) is strictly configured to allow only authorized frontend origins to communicate with the API.

### 4. Environment Security
- **Secret Management**: All sensitive configurations (Database URLs, API Keys) are managed via Environment Variables and are excluded from version control to prevent accidental leaks.

## 🚀 Quick Start (Docker)

The system is fully containerized using Docker Compose. Ensure Docker is running on your machine before starting.


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