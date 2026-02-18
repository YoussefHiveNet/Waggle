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
