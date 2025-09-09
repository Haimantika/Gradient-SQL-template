# SQL Agent with Synthetic Data Generation

A Gradient AI-powered agent that generates realistic mock datasets and produces safe SQL INSERT scripts. Designed for developers and testers to bootstrap staging environments with synthetic data without touching production systems.

> **Based on**: [DigitalOcean Gradient Agent Templates - SQL Agent](https://github.com/digitalocean/gradient-agent-templates/tree/main/sql-agent)  
> **Enhanced with**: Synthetic data generation capabilities for safe testing and development

## Features
- **Gradient AI Integration**: Natural language processing for data generation requests
- **Synthetic Data Generation**: users, orders, payments, products, and custom schemas
- **Multiple Output Formats**: SQL INSERT statements, CSV, and JSON exports
- **Safety First**: Never touches production data; designed for staging/test bootstraps
- **Interactive Chat**: Conversational interface for data generation and SQL assistance

## Requirements
- Python 3.10+
- DigitalOcean account and Gradient AI credentials
- `pip install -r requirements.txt`

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Gradient AI Credentials
```bash
cp env.example .env
# Edit .env and add your Gradient AI credentials:
# GRADIENT_ACCESS_TOKEN=your_token_here
# GRADIENT_WORKSPACE_ID=your_workspace_id_here
```

### 3. Run the Interactive Agent
```bash
python3 main.py
```

### 4. Start Chatting!
Type natural language requests like:
- "Generate 10 mock users with random names and emails"
- "Create 20 orders with amounts between $10-$500 in 2024"
- "Give me 5 failed payment transactions"
- "Export 15 products as CSV"

## Project Structure
- `src/synthetic_data_generator.py` - Core data generator
- `src/sql_tools.py` - SQL safety helpers (SELECT-only logic, formatting)
- `src/agent.py` - Interactive agent (uses Gradient AI)
- `src/config.py` - Env settings
- `main.py` - Optional agent entrypoint

## Relationship to Original Template

This project extends the [DigitalOcean Gradient Agent Templates SQL Agent](https://github.com/digitalocean/gradient-agent-templates/tree/main/sql-agent) with:

- **Synthetic Data Generation**: Create realistic mock datasets without touching production data
- **Multiple Output Formats**: SQL INSERT statements, CSV, and JSON exports
- **Enhanced Safety**: Production data protection and query validation
- **Standalone Operation**: Works independently for data generation
- **Custom Schema Support**: Generate data for any table structure

The original template focuses on querying existing databases, while this enhanced version focuses on **generating safe test data** for development and staging environments.

## Notes
- This repo is trimmed for core functionality only.
- Use `env.example` as a guide; never commit real `.env` files.
- Generated data is synthetic; do not treat as real user information. 
