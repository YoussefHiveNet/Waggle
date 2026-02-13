# Hivenet Analytics – Cube + MCP Server

## 📌 What is this project?

This project is an AI-ready analytics stack that connects:
- BigQuery (data warehouse)
- Cube (semantic layer)
- MCP Server (AI tools layer using FastMCP)

The goal of the project is to enable an AI Data Analyst agent to:
- Query business metrics through a semantic layer (Cube)
- Avoid direct raw SQL on BigQuery
- Validate analytics data safely
- Expose structured analytics tools via an MCP server

**Main dataset:**  
`waggle_sandbox.business_pulse_weekly_reporting`

**Main cube:**  
`business_pulse_weekly_reporting`

---

## 🏗️ Architecture

```
BigQuery (Database)
    ↓
Cube (Semantic Layer / API)
    ↓
MCP Server (FastMCP Tools)
    ↓
AI Analyst / Chatwise / Claude
```

**Tech Stack:**
- Cube (Semantic analytics layer)
- FastMCP (tool server)
- Docker (containerization)
- BigQuery (data warehouse)
- Google Cloud (deployment target)

---

## 📁 Project Structure (Typical)

```
.
├── cube/
│   ├── model/
│   ├── schema/
│   ├── package.json
│   └── Dockerfile
│
├── mcp/
│   ├── main.py
│   ├── cube_client.py
│   └── requirements.txt
│
└── README.md
```

---

## 🐳 How to Start Cube (Docker)

### 1. Go to the Cube directory
```bash
cd cube
```

### 2. Build the Cube image
```bash
docker build -t cube .
```

### 3. Run Cube with DEV MODE (IMPORTANT)
```bash
docker run -p 4000:4000 \
  -e CUBEJS_DEV_MODE=true \
  -e CUBEJS_DB_TYPE=bigquery \
  -e CUBEJS_DB_BQ_PROJECT_ID=YOUR_PROJECT_ID \
  -e CUBEJS_DB_BQ_DATASET=YOUR_DATASET \
  -e CUBEJS_API_SECRET=super-secret-change-later \
  cube
```

Cube API will be available at:
```
http://localhost:4000/cubejs-api/v1
```

### 4. Test Cube is running
```bash
curl http://localhost:4000/cubejs-api/v1/meta
```

## 🚀 How to Start the MCP Server

### 1. Go to the MCP directory
```bash
cd mcp
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the MCP server
```bash
python main.py
```

Alternative (if using uvicorn explicitly):
```bash
uvicorn main:app --host 0.0.0.0 --port 3333
```

**Expected logs:**
```
INFO: MCP server started
INFO: Connected to Cube at http://cube:4000/cubejs-api/v1
```

## 🔗 Cube URL Configuration (VERY IMPORTANT)

Inside `main.py`:
```python
CUBE_URL = "http://cube:4000/cubejs-api/v1"
```

**Use:**
- `http://cube:4000` → if using Docker network
- `http://localhost:4000` → if running locally

---

## 🔧 Required Environment Variables

### Cube Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| CUBEJS_DEV_MODE | Enables schema hot reload | YES (true) |
| CUBEJS_DB_TYPE | Database type | YES (bigquery) |
| CUBEJS_DB_BQ_PROJECT_ID | GCP Project ID | YES |
| CUBEJS_DB_BQ_DATASET | BigQuery Dataset | YES |
| CUBEJS_API_SECRET | API security key | YES |

**Example:**
```
CUBEJS_DEV_MODE=true
CUBEJS_DB_TYPE=bigquery
CUBEJS_DB_BQ_PROJECT_ID=data-sandbox-xxxx
CUBEJS_DB_BQ_DATASET=waggle_sandbox
CUBEJS_API_SECRET=super-secret-change-later
```

---

## 📊 Cube Model Description

**Primary cube:** `business_pulse_weekly_reporting`

**SQL table:** `waggle_sandbox.business_pulse_weekly_reporting`

**Contains:**
- `reportingWeek` (time dimension)
- Weekly KPIs
- Aggregated business metrics
- Reporting-ready semantic fields

This allows the AI agent to query metrics safely without directly querying raw tables.

---

## 🧪 Common Development Tasks

### 1. Check Cube Metadata
```bash
curl http://localhost:4000/cubejs-api/v1/meta
```

### 2. Run a Test Query
```bash
curl -X POST http://localhost:4000/cubejs-api/v1/load \
  -H "Content-Type: application/json" \
  -d '{
    "measures": ["business_pulse_weekly_reporting.count"]
  }'
```

### 3. Validate Data Against BigQuery
Run in BigQuery:
```sql
SELECT *
FROM waggle_sandbox.business_pulse_weekly_reporting
LIMIT 10;
```

Then compare:
- Row counts
- Aggregations
- Dates
- Filters

---

## 🔍 Data Validation Workflow (For AI Analyst)

Recommended process:
1. Query metric from Cube API
2. Write equivalent SQL in BigQuery
3. Compare results
4. Confirm semantic layer correctness
5. Flag mismatches if any

This is used to validate AI-generated analytics answers.

---

## ⚠️ Common Problems & Fixes

### ❌ Error: HTTP 404 when calling Cube
**Cause:** Wrong Cube API URL

**Fix:**
```python
CUBE_URL = "http://localhost:4000/cubejs-api/v1"
```
Or (docker):
```python
CUBE_URL = "http://cube:4000/cubejs-api/v1"
```

### ❌ MCP Server cannot connect to Cube
**Checklist:**
- Cube container is running
- Port 4000 is exposed
- Correct hostname (`cube` vs `localhost`)
- Same Docker network (if containerized)

### ❌ Docker not running / Docker API error
**Error example:**
```
failed to connect to the docker API
```
**Fix:**
- Start Docker Desktop
- Ensure Linux engine is running
- Restart Docker service

### ❌ Cube cannot connect to BigQuery
**Fix checklist:**
- Service account has BigQuery permissions
- Correct project ID
- Correct dataset name
- Credentials properly configured in environment

### ❌ Schema changes not updating
**Fix:** Make sure dev mode is enabled:
```
CUBEJS_DEV_MODE=true
```
Without dev mode, Cube will not hot reload schema changes.

---

## ☁️ Deployment Notes (Cloud Run / GCP)

When deploying to cloud:
- Set PORT correctly (8080 or 4000)
- Add BigQuery IAM permissions
- Configure environment variables
- Allow unauthenticated access if needed
- Ensure service account has BigQuery read access

---

## 🧠 What the MCP Server Actually Does

The MCP server:
- Connects to Cube API
- Exposes analytics tools (metadata, queries)
- Acts as a bridge between AI agents and Cube
- Standardizes analytics access for LLMs
- Prevents unsafe direct DB querying

**Example tools:**
- `get_cube_meta()`
- `run_cube_query()`
- Analytics validation tools

---

## 👤 Intended Users

- AI Data Analyst agents
- Analytics Engineers
- Data Engineers
- Internal validation workflows

---

## 📝 Final Notes

This project is designed for:
- Semantic analytics
- AI-driven data analysis
- Safe metric querying
- Scalable cloud deployment

If Cube + MCP + BigQuery are all running correctly, the AI agent can reliably query business metrics, validate answers, and perform analytics without directly accessing raw database tables.
