# 🤖 Agentic AI Sales Forecasting System

An AI-powered sales forecasting system that uses a **multi-agent architecture** to analyze historical sales data, generate future sales predictions, verify prediction quality, and produce business insights.

The system combines **FastAPI, React, Machine Learning, and Agentic AI** into an end-to-end application.

---

## 📌 Project Overview

The Agentic AI Sales Forecasting System automates the sales forecasting workflow using multiple specialized AI agents.

Instead of using a single prediction process, the system divides the workflow into multiple agents:

1. Data Collection Agent
2. Data Processing Agent
3. Prediction Agent
4. Verification Agent
5. Report Agent
6. Orchestrator Agent

The **Orchestrator Agent** coordinates the complete workflow and manages communication between the agents.

---

## 🎯 Objectives

The main objectives of this project are:

- Analyze historical sales data.
- Clean and preprocess sales data automatically.
- Generate future sales forecasts.
- Validate prediction accuracy.
- Detect potential forecasting issues.
- Generate business insights automatically.
- Provide an easy-to-use web dashboard.
- Demonstrate a practical multi-agent AI architecture.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │   Frontend Dashboard │
                    └──────────┬───────────┘
                               │
                               │ HTTP Request
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │   Orchestrator Agent    │
                  └────────────┬────────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
     │ Data         │  │ Data         │  │ Prediction   │
     │ Collection   │  │ Processing   │  │ Agent        │
     │ Agent        │  │ Agent        │  │              │
     └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                     ┌─────────────────┐
                     │ Verification    │
                     │ Agent           │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Report Agent    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Forecast +      │
                     │ Business        │
                     │ Insights        │
                     └─────────────────┘