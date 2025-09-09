"""Main SQL Agent with synthetic data generation capabilities."""

import re
from typing import Dict, Any, List, Optional, Tuple
from gradientai import Gradient
from .config import settings
from .sql_tools import SQLTools


class SQLAgent:
    """SQL Agent with synthetic data generation capabilities."""
    
    def __init__(self):
        """Initialize the SQL Agent."""
        self.gradient = Gradient(
            access_token=settings.gradient_access_token,
            workspace_id=settings.gradient_workspace_id
        )
        self.sql_tools = SQLTools()
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent."""
        return """You are a SQL Agent with synthetic data generation capabilities. Your role is to help developers and testers create safe mock datasets and SQL queries without touching production data.

CORE CAPABILITIES:
1. Generate synthetic data (users, orders, payments, products, custom schemas)
2. Create SQL INSERT statements for mock data
3. Export data as CSV format
4. Execute safe SQL queries (SELECT only, with safety checks)
5. Provide database schema information

SAFETY RULES:
- NEVER execute INSERT, UPDATE, DELETE, DROP, or other destructive operations
- NEVER connect to production databases unless explicitly allowed
- Always validate queries for safety before execution
- Limit generated records to prevent resource exhaustion
- Never expose real customer data

SYNTHETIC DATA GENERATION:
- Users: Generate mock users with names, emails, phones, addresses
- Orders: Create orders with amounts, dates, statuses, product info
- Payments: Generate payment transactions including failed ones
- Products: Create product catalogs with prices, categories, SKUs
- Custom: Generate data based on user-defined schemas

OUTPUT FORMATS:
- SQL: INSERT statements ready for execution
- CSV: Comma-separated values for import
- JSON: Structured data format

When users ask for data generation, always:
1. Confirm the number of records (respect max limits)
2. Specify the output format
3. Generate the data safely
4. Provide clear instructions for use

Example interactions:
- "Generate 10 mock users" → SQL INSERT statements for users table
- "Create 20 orders with amounts $10-500" → INSERT statements with specified criteria
- "Give me 5 failed payment transactions" → INSERT statements for failed payments
- "Export 50 products as CSV" → CSV format data

Always prioritize safety and provide helpful, accurate responses."""

    def _parse_generation_request(self, user_input: str) -> Dict[str, Any]:
        """Parse user input to extract generation parameters.
        
        Args:
            user_input: User's request
            
        Returns:
            Dictionary with parsed parameters
        """
        user_input_lower = user_input.lower()
        
        # Extract count
        count_match = re.search(r'(\d+)\s*(?:mock|fake|test)?\s*(?:users?|orders?|payments?|products?|records?)', user_input_lower)
        count = int(count_match.group(1)) if count_match else 10
        
        # Extract data type
        data_type = 'users'
        if 'order' in user_input_lower:
            data_type = 'orders'
        elif 'payment' in user_input_lower or 'transaction' in user_input_lower:
            data_type = 'payments'
        elif 'product' in user_input_lower:
            data_type = 'products'
        elif 'user' in user_input_lower:
            data_type = 'users'
        
        # Extract format
        format_type = 'sql'
        if 'csv' in user_input_lower:
            format_type = 'csv'
        elif 'json' in user_input_lower:
            format_type = 'json'
        
        # Extract amount range for orders
        amount_range = (10, 500)
        amount_match = re.search(r'\$?(\d+)\s*[-–]\s*\$?(\d+)', user_input)
        if amount_match:
            amount_range = (float(amount_match.group(1)), float(amount_match.group(2)))
        
        # Extract year
        year = None
        year_match = re.search(r'(\d{4})', user_input)
        if year_match:
            year = int(year_match.group(1))
        
        # Check for failed payments
        include_failed = 'failed' in user_input_lower
        
        return {
            'count': count,
            'data_type': data_type,
            'format_type': format_type,
            'amount_range': amount_range,
            'year': year,
            'include_failed': include_failed
        }
    
    def generate_synthetic_data(self, user_input: str) -> str:
        """Generate synthetic data based on user request.
        
        Args:
            user_input: User's request for data generation
            
        Returns:
            Generated data in requested format
        """
        try:
            params = self._parse_generation_request(user_input)
            
            if params['data_type'] == 'users':
                return self.sql_tools.generate_mock_users(
                    params['count'], 
                    params['format_type']
                )
            
            elif params['data_type'] == 'orders':
                return self.sql_tools.generate_mock_orders(
                    params['count'],
                    params['amount_range'],
                    params['year'],
                    params['format_type']
                )
            
            elif params['data_type'] == 'payments':
                if params['include_failed']:
                    return self.sql_tools.generate_failed_payments(
                        params['count'],
                        params['format_type']
                    )
                else:
                    # Generate regular payment transactions
                    transactions = self.sql_tools.generator.generate_payment_transactions(
                        params['count']
                    )
                    if params['format_type'] == 'sql':
                        inserts = self.sql_tools.generator.to_sql_inserts(
                            transactions, 'payment_transactions'
                        )
                        return '\n'.join(inserts)
                    elif params['format_type'] == 'csv':
                        return self.sql_tools.generator.to_csv(transactions)
                    else:
                        return str(transactions)
            
            elif params['data_type'] == 'products':
                products = self.sql_tools.generator.generate_products(params['count'])
                if params['format_type'] == 'sql':
                    inserts = self.sql_tools.generator.to_sql_inserts(products, 'products')
                    return '\n'.join(inserts)
                elif params['format_type'] == 'csv':
                    return self.sql_tools.generator.to_csv(products)
                else:
                    return str(products)
            
            else:
                return f"Unknown data type: {params['data_type']}"
                
        except Exception as e:
            return f"Error generating data: {str(e)}"
    
    def execute_sql_query(self, query: str) -> str:
        """Execute a SQL query with safety checks.
        
        Args:
            query: SQL query to execute
            
        Returns:
            Query results or error message
        """
        success, message, results = self.sql_tools.execute_safe_query(query)
        
        if success:
            if results:
                # Format results nicely
                if len(results) == 0:
                    return "Query executed successfully. No rows returned."
                else:
                    formatted_results = f"Query executed successfully. {len(results)} rows returned:\n\n"
                    for i, row in enumerate(results[:10]):  # Limit to first 10 rows
                        formatted_results += f"Row {i+1}: {row}\n"
                    if len(results) > 10:
                        formatted_results += f"\n... and {len(results) - 10} more rows"
                    return formatted_results
            else:
                return message
        else:
            return f"Query execution failed: {message}"
    
    def get_database_info(self) -> str:
        """Get information about the connected database.
        
        Returns:
            Database information string
        """
        if not self.sql_tools.engine:
            return "No database connection available. Set DATABASE_URL in your environment to connect to a database."
        
        tables = self.sql_tools.list_tables()
        if not tables:
            return "Connected to database but no tables found."
        
        info = f"Connected to database. Found {len(tables)} tables:\n\n"
        for table in tables:
            schema = self.sql_tools.get_table_schema(table)
            if schema:
                info += f"Table: {table}\n"
                for col in schema['columns']:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    info += f"  - {col['name']}: {col['type']} {nullable}\n"
                info += "\n"
        
        return info
    
    def chat(self, user_input: str) -> str:
        """Main chat interface for the agent.
        
        Args:
            user_input: User's message
            
        Returns:
            Agent's response
        """
        user_input_lower = user_input.lower()
        
        # Check if this is a data generation request
        generation_keywords = ['generate', 'create', 'mock', 'fake', 'test data', 'synthetic']
        if any(keyword in user_input_lower for keyword in generation_keywords):
            return self.generate_synthetic_data(user_input)
        
        # Check if this is a SQL query
        sql_keywords = ['select', 'show', 'describe', 'explain']
        if any(keyword in user_input_lower for keyword in sql_keywords):
            return self.execute_sql_query(user_input)
        
        # Check if this is a database info request
        if any(keyword in user_input_lower for keyword in ['tables', 'schema', 'database info', 'show tables']):
            return self.get_database_info()
        
        # Use Gradient AI for general SQL assistance
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.gradient.chat_complete(
                model="nous-hermes-2-mixtral-8x7b-dpo",
                messages=messages,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def run_interactive(self):
        """Run the agent in interactive mode."""
        print("SQL Agent with Synthetic Data Generation")
        print("=" * 50)
        print("Type 'quit' to exit, 'help' for examples")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if not user_input:
                    continue
                
                response = self.chat(user_input)
                print(f"Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
SQL Agent Help
==============

DATA GENERATION EXAMPLES:
- "Generate 10 mock users" → SQL INSERT statements for users
- "Create 20 orders with amounts $10-500" → Orders with specified amount range
- "Give me 5 failed payment transactions" → Failed payment records
- "Generate 15 products as CSV" → Product data in CSV format
- "Create 50 users for 2024" → Users with 2024 creation dates

SQL QUERIES:
- "SELECT * FROM users LIMIT 5" → Execute safe SELECT queries
- "SHOW TABLES" → List all tables in database
- "DESCRIBE users" → Show table schema

DATABASE INFO:
- "Show database info" → Display connected database information
- "List tables" → Show all available tables

SAFETY FEATURES:
- Only SELECT queries are executed
- No production data exposure
- Automatic query validation
- Record count limits

Type 'quit' to exit.
"""
        print(help_text)
