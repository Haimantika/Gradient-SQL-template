# SQL Agent with Synthetic Data Generation

A Gradient AI-powered agent that generates realistic mock datasets and produces safe SQL INSERT scripts. Designed for developers and testers to bootstrap staging environments with synthetic data without touching production systems.

> **Based on**: [DigitalOcean Gradient Agent Templates - SQL Agent](https://github.com/digitalocean/gradient-agent-templates/tree/main/sql-agent)  
> **Enhanced with**: Synthetic data generation capabilities for safe testing and development

## Features

- **Natural Language Chat**: Conversational interface for data generation requests
- **Synthetic Data Generation**: users, orders, payments, products, and custom schemas
- **Multiple Output Formats**: SQL INSERT statements, CSV, and JSON exports
- **Safety First**: Never touches production data; designed for staging/test bootstraps
- **Real-time Generation**: Instant data creation with live preview
- **Dual Interface**: Both chat and manual configuration options

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

Open http://localhost:8501 in your browser.

### 4. Generate Data
Use the Chat Interface tab to type natural language requests like:
- "Generate 10 mock users with random names and emails"
- "Create 20 orders with amounts between $10-$500 in 2024"
- "Give me 5 failed payment transactions"
- "Export 15 products as CSV"

### Alternative: Command Line Interface
```bash
python3 main.py
```

## Web UI Features

### Chat Interface
The web UI features a conversational chat interface for data generation:

- **Natural Language Processing**: Type requests in plain English
- **Smart Understanding**: Interprets your data generation needs
- **Instant Generation**: Get SQL, CSV, or JSON output immediately
- **Real-time Responses**: Interactive conversation flow

### Manual Configuration Interface
For precise control, use the manual configuration tab:

- **One-Click Generation**: Quick buttons for common scenarios
- **Data Visualization**: Interactive tables and previews
- **Multiple Downloads**: SQL, CSV, and JSON export options
- **Easy Configuration**: Sidebar controls for all parameters

### Quick Actions
- **10 Users** - Generate users with random names and emails
- **20 Orders ($10-$500)** - Create orders with specified amount range
- **5 Failed Payments** - Generate failed payment transactions
- **15 Products (CSV)** - Export products in CSV format

## Project Structure

- `src/synthetic_data_generator.py` - Core data generator
- `src/sql_tools.py` - SQL safety helpers and formatting
- `src/agent.py` - Interactive agent
- `src/config.py` - Environment settings
- `main.py` - Command-line entrypoint
- `app.py` - Streamlit web UI

## Usage Examples

### Generate Users
```
Generate 50 users with realistic addresses and phone numbers
```

### Create Orders
```
Create 20 orders with amounts between $10-$500 in 2024
```

### Failed Payments
```
Give me 5 failed payment transactions
```

### Export Data
```
Export 15 products as CSV
```

## Safety Features

- Never touches production data
- Generates realistic but fake data
- Safe for staging and development environments
- Multiple output formats available

## Notes

- Use `env.example` as a guide; never commit real `.env` files
- Generated data is synthetic; do not treat as real user information
- The chat interface works with or without Gradient AI credentials