"""SQL tools for the agent."""

import re
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from .config import settings
from .synthetic_data_generator import SyntheticDataGenerator


class SQLTools:
    """Tools for SQL operations and safety checks."""
    
    def __init__(self):
        """Initialize SQL tools."""
        self.generator = SyntheticDataGenerator()
        self.engine = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize database engine if database URL is provided."""
        if settings.database_url:
            try:
                self.engine = create_engine(settings.database_url)
                # Test connection
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            except SQLAlchemyError as e:
                print(f"Warning: Could not connect to database: {e}")
                self.engine = None
    
    def is_safe_query(self, query: str) -> Tuple[bool, str]:
        """Check if a query is safe to execute.
        
        Args:
            query: SQL query to check
            
        Returns:
            Tuple of (is_safe, reason)
        """
        query_lower = query.lower().strip()
        
        # Check for dangerous operations
        dangerous_patterns = [
            r'\b(drop|delete|truncate|alter|create|insert|update)\b',
            r'\b(exec|execute|sp_|xp_)\b',
            r'--',  # SQL comments
            r'/\*.*?\*/',  # Block comments
            r'union\s+select',  # SQL injection patterns
            r'information_schema',
            r'sys\.',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return False, f"Query contains potentially dangerous pattern: {pattern}"
        
        # Check for production database indicators
        production_indicators = [
            'prod', 'production', 'live', 'main'
        ]
        
        for indicator in production_indicators:
            if indicator in query_lower:
                if not settings.allow_production_connections:
                    return False, f"Query references production environment: {indicator}"
        
        return True, "Query appears safe"
    
    def generate_mock_users(self, count: int, format_type: str = 'sql') -> str:
        """Generate mock users in specified format.
        
        Args:
            count: Number of users to generate
            format_type: Output format ('sql', 'csv', 'json')
            
        Returns:
            Generated data in specified format
        """
        if count > settings.max_generated_records:
            return f"Error: Cannot generate more than {settings.max_generated_records} records"
        
        users = self.generator.generate_users(count)
        
        if format_type.lower() == 'sql':
            inserts = self.generator.to_sql_inserts(users, 'users')
            return '\n'.join(inserts)
        elif format_type.lower() == 'csv':
            return self.generator.to_csv(users)
        else:
            return str(users)
    
    def generate_mock_orders(self, count: int, amount_range: Tuple[float, float] = (10, 500),
                           year: Optional[int] = None, format_type: str = 'sql') -> str:
        """Generate mock orders in specified format.
        
        Args:
            count: Number of orders to generate
            amount_range: Tuple of (min_amount, max_amount)
            year: Specific year for orders
            format_type: Output format ('sql', 'csv', 'json')
            
        Returns:
            Generated data in specified format
        """
        if count > settings.max_generated_records:
            return f"Error: Cannot generate more than {settings.max_generated_records} records"
        
        orders = self.generator.generate_orders(count, amount_range=amount_range, year=year)
        
        if format_type.lower() == 'sql':
            inserts = self.generator.to_sql_inserts(orders, 'orders')
            return '\n'.join(inserts)
        elif format_type.lower() == 'csv':
            return self.generator.to_csv(orders)
        else:
            return str(orders)
    
    def generate_failed_payments(self, count: int, format_type: str = 'sql') -> str:
        """Generate mock failed payment transactions.
        
        Args:
            count: Number of failed transactions to generate
            format_type: Output format ('sql', 'csv', 'json')
            
        Returns:
            Generated data in specified format
        """
        if count > settings.max_generated_records:
            return f"Error: Cannot generate more than {settings.max_generated_records} records"
        
        # Generate more transactions to ensure we get enough failed ones
        all_transactions = self.generator.generate_payment_transactions(count * 2, include_failed=True)
        failed_transactions = [t for t in all_transactions if t['status'] == 'failed'][:count]
        
        if format_type.lower() == 'sql':
            inserts = self.generator.to_sql_inserts(failed_transactions, 'payment_transactions')
            return '\n'.join(inserts)
        elif format_type.lower() == 'csv':
            return self.generator.to_csv(failed_transactions)
        else:
            return str(failed_transactions)
    
    def generate_custom_data(self, schema: Dict[str, Any], count: int, 
                           table_name: str, format_type: str = 'sql') -> str:
        """Generate custom data based on schema.
        
        Args:
            schema: Dictionary defining field types and constraints
            count: Number of records to generate
            table_name: Name of the table
            format_type: Output format ('sql', 'csv', 'json')
            
        Returns:
            Generated data in specified format
        """
        if count > settings.max_generated_records:
            return f"Error: Cannot generate more than {settings.max_generated_records} records"
        
        data = self.generator.generate_custom_data(schema, count)
        
        if format_type.lower() == 'sql':
            inserts = self.generator.to_sql_inserts(data, table_name)
            return '\n'.join(inserts)
        elif format_type.lower() == 'csv':
            return self.generator.to_csv(data)
        else:
            return str(data)
    
    def execute_safe_query(self, query: str) -> Tuple[bool, str, Optional[List[Dict]]]:
        """Execute a query if it's deemed safe.
        
        Args:
            query: SQL query to execute
            
        Returns:
            Tuple of (success, message, results)
        """
        if not self.engine:
            return False, "No database connection available", None
        
        is_safe, reason = self.is_safe_query(query)
        if not is_safe:
            return False, f"Query rejected: {reason}", None
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                
                # Handle different types of queries
                if query.strip().lower().startswith('select'):
                    rows = result.fetchall()
                    columns = result.keys()
                    results = [dict(zip(columns, row)) for row in rows]
                    return True, f"Query executed successfully. {len(results)} rows returned.", results
                else:
                    conn.commit()
                    return True, "Query executed successfully.", None
                    
        except SQLAlchemyError as e:
            return False, f"Database error: {str(e)}", None
    
    def get_table_schema(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing schema information
        """
        if not self.engine:
            return None
        
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            
            schema = {
                'table_name': table_name,
                'columns': []
            }
            
            for col in columns:
                schema['columns'].append({
                    'name': col['name'],
                    'type': str(col['type']),
                    'nullable': col['nullable'],
                    'default': col.get('default')
                })
            
            return schema
            
        except SQLAlchemyError:
            return None
    
    def list_tables(self) -> List[str]:
        """List all tables in the database.
        
        Returns:
            List of table names
        """
        if not self.engine:
            return []
        
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except SQLAlchemyError:
            return []
