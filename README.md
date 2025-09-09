# SQL Agent with Synthetic Data Generation

A Gradient AI-powered agent that generates realistic mock datasets and produces safe SQL INSERT scripts. Designed for developers and testers to bootstrap staging environments with synthetic data without touching production systems.

> **Based on**: [DigitalOcean Gradient Agent Templates - SQL Agent](https://github.com/digitalocean/gradient-agent-templates/tree/main/sql-agent)  
> **Enhanced with**: Synthetic data generation capabilities for safe testing and development

## Features
- **🤖 Natural Language Chat**: Conversational AI interface for data generation requests
- **🧠 Gradient AI Integration**: Smart understanding of complex data generation needs
- **📊 Synthetic Data Generation**: users, orders, payments, products, and custom schemas
- **💾 Multiple Output Formats**: SQL INSERT statements, CSV, and JSON exports
- **🔒 Safety First**: Never touches production data; designed for staging/test bootstraps
- **⚡ Real-time Generation**: Instant data creation with live preview
- **🎯 Dual Interface**: Both chat and manual configuration options

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

### 3. Launch the Web UI (Recommended)
```bash
python3 -m streamlit run app.py
```

### 4. Start Chatting!
Open http://localhost:8501 and use the **🤖 Chat Interface** tab to type natural language requests like:
- "Generate 10 mock users with random names and emails"
- "Create 20 orders with amounts between $10-$500 in 2024"
- "Give me 5 failed payment transactions"
- "Export 15 products as CSV"

### Alternative: Command Line Interface
```bash
python3 main.py
```

## 🌐 Web UI (Streamlit)

For the best experience, use the Streamlit web interface with **natural language chat**:

```bash
python3 -m streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### 🤖 Natural Language Chat Interface
The web UI features a **conversational chat interface** powered by Gradient AI:

- **💬 Chat with the AI**: Type natural language requests
- **🧠 Smart Understanding**: AI interprets your data generation needs
- **⚡ Instant Generation**: Get SQL, CSV, or JSON output immediately
- **🔄 Real-time Responses**: Interactive conversation flow

**Example Chat Interactions:**
- "Generate 10 mock users with random names and emails"
- "Create 20 orders with amounts between $10-$500 in 2024"
- "Give me 5 failed payment transactions"
- "Export 15 products as CSV"
- "Make 50 users with realistic addresses and phone numbers"

### ⚙️ Manual Configuration Interface
For precise control, use the manual configuration tab:

- **🎯 One-Click Generation**: Quick buttons for common scenarios
- **📊 Data Visualization**: Interactive tables and previews
- **💾 Multiple Downloads**: SQL, CSV, and JSON export options
- **⚙️ Easy Configuration**: Sidebar controls for all parameters
- **🔒 Safety Indicators**: Clear safety features highlighted

### Quick Actions in UI:
- 👥 **10 Users** - Generate users with random names and emails
- 🛒 **20 Orders ($10-$500)** - Create orders with specified amount range
- 💳 **5 Failed Payments** - Generate failed payment transactions
- 📦 **15 Products (CSV)** - Export products in CSV format

## Project Structure
- `src/synthetic_data_generator.py` - Core data generator
- `src/sql_tools.py` - SQL safety helpers (SELECT-only logic, formatting)
- `src/agent.py` - Interactive agent (uses Gradient AI)
- `src/config.py` - Env settings
- `main.py` - Command-line agent entrypoint
- `app.py` - Streamlit web UI

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
