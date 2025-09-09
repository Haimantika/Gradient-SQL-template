"""Synthetic data generation for SQL Agent."""

import random
import csv
import io
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from faker import Faker
# Using built-in Faker methods instead of specific providers
import pandas as pd


class SyntheticDataGenerator:
    """Generates synthetic data for testing and development."""
    
    def __init__(self, locale: str = 'en_US'):
        """Initialize the generator with a specific locale."""
        self.fake = Faker(locale)
    
    def generate_users(self, count: int, include_fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Generate mock user data.
        
        Args:
            count: Number of users to generate
            include_fields: Specific fields to include (default: all)
            
        Returns:
            List of user dictionaries
        """
        if include_fields is None:
            include_fields = ['id', 'name', 'email', 'phone', 'address', 'created_at']
        
        users = []
        for i in range(count):
            user = {}
            
            if 'id' in include_fields:
                user['id'] = i + 1
            if 'name' in include_fields:
                user['name'] = self.fake.name()
            if 'email' in include_fields:
                user['email'] = self.fake.email()
            if 'phone' in include_fields:
                user['phone'] = self.fake.phone_number()
            if 'address' in include_fields:
                user['address'] = self.fake.address().replace('\n', ', ')
            if 'created_at' in include_fields:
                user['created_at'] = self.fake.date_time_between(start_date='-2y', end_date='now')
            
            users.append(user)
        
        return users
    
    def generate_orders(self, count: int, user_ids: Optional[List[int]] = None, 
                       amount_range: tuple = (10, 500), 
                       year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Generate mock order data.
        
        Args:
            count: Number of orders to generate
            user_ids: List of user IDs to assign orders to (random if None)
            amount_range: Tuple of (min_amount, max_amount)
            year: Specific year for orders (current year if None)
            
        Returns:
            List of order dictionaries
        """
        orders = []
        start_date = datetime(year, 1, 1) if year else datetime.now().replace(month=1, day=1)
        end_date = datetime(year, 12, 31) if year else datetime.now()
        
        for i in range(count):
            order = {
                'id': i + 1,
                'user_id': random.choice(user_ids) if user_ids else random.randint(1, 100),
                'amount': round(random.uniform(amount_range[0], amount_range[1]), 2),
                'status': random.choice(['pending', 'completed', 'cancelled', 'shipped']),
                'order_date': self.fake.date_time_between(start_date=start_date, end_date=end_date),
                'product_name': self.fake.word() + ' ' + self.fake.word(),
                'quantity': random.randint(1, 10)
            }
            orders.append(order)
        
        return orders
    
    def generate_payment_transactions(self, count: int, 
                                   transaction_types: Optional[List[str]] = None,
                                   include_failed: bool = True) -> List[Dict[str, Any]]:
        """Generate mock payment transaction data.
        
        Args:
            count: Number of transactions to generate
            transaction_types: List of transaction types (default: common types)
            include_failed: Whether to include failed transactions
            
        Returns:
            List of transaction dictionaries
        """
        if transaction_types is None:
            transaction_types = ['credit_card', 'debit_card', 'paypal', 'bank_transfer']
        
        transactions = []
        for i in range(count):
            is_failed = include_failed and random.random() < 0.1  # 10% failure rate
            
            transaction = {
                'id': i + 1,
                'order_id': random.randint(1, 1000),
                'amount': round(random.uniform(5, 1000), 2),
                'payment_method': random.choice(transaction_types),
                'status': 'failed' if is_failed else random.choice(['completed', 'pending', 'refunded']),
                'transaction_date': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'gateway': random.choice(['stripe', 'paypal', 'square', 'authorize_net']),
                'failure_reason': random.choice(['insufficient_funds', 'card_declined', 'network_error']) if is_failed else None
            }
            transactions.append(transaction)
        
        return transactions
    
    def generate_products(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock product data.
        
        Args:
            count: Number of products to generate
            
        Returns:
            List of product dictionaries
        """
        products = []
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty']
        
        for i in range(count):
            product = {
                'id': i + 1,
                'name': self.fake.word() + ' ' + self.fake.word(),
                'description': self.fake.text(max_nb_chars=200),
                'price': round(random.uniform(10, 1000), 2),
                'category': random.choice(categories),
                'sku': self.fake.bothify(text='???-###-???'),
                'stock_quantity': random.randint(0, 100),
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now')
            }
            products.append(product)
        
        return products
    
    def to_sql_inserts(self, data: List[Dict[str, Any]], table_name: str) -> List[str]:
        """Convert data to SQL INSERT statements.
        
        Args:
            data: List of dictionaries containing the data
            table_name: Name of the table to insert into
            
        Returns:
            List of SQL INSERT statements
        """
        if not data:
            return []
        
        insert_statements = []
        columns = list(data[0].keys())
        columns_str = ', '.join(columns)
        
        for record in data:
            values = []
            for col in columns:
                value = record[col]
                if value is None:
                    values.append('NULL')
                elif isinstance(value, str):
                    # Escape single quotes in strings
                    escaped_value = value.replace("'", "''")
                    values.append(f"'{escaped_value}'")
                elif isinstance(value, datetime):
                    values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                else:
                    values.append(str(value))
            
            values_str = ', '.join(values)
            insert_statements.append(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});")
        
        return insert_statements
    
    def to_csv(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> Union[str, bytes]:
        """Convert data to CSV format.
        
        Args:
            data: List of dictionaries containing the data
            filename: Optional filename to save to (returns bytes if None)
            
        Returns:
            CSV content as string or bytes
        """
        if not data:
            return ""
        
        df = pd.DataFrame(data)
        
        if filename:
            df.to_csv(filename, index=False)
            return f"CSV file saved as {filename}"
        else:
            output = io.StringIO()
            df.to_csv(output, index=False)
            return output.getvalue()
    
    def generate_custom_data(self, schema: Dict[str, Any], count: int) -> List[Dict[str, Any]]:
        """Generate custom data based on a schema definition.
        
        Args:
            schema: Dictionary defining field types and constraints
            count: Number of records to generate
            
        Returns:
            List of generated records
        """
        records = []
        
        for i in range(count):
            record = {}
            
            for field_name, field_config in schema.items():
                field_type = field_config.get('type', 'string')
                constraints = field_config.get('constraints', {})
                
                if field_type == 'id':
                    record[field_name] = i + 1
                elif field_type == 'name':
                    record[field_name] = self.fake.name()
                elif field_type == 'email':
                    record[field_name] = self.fake.email()
                elif field_type == 'phone':
                    record[field_name] = self.fake.phone_number()
                elif field_type == 'address':
                    record[field_name] = self.fake.address().replace('\n', ', ')
                elif field_type == 'amount':
                    min_val = constraints.get('min', 0)
                    max_val = constraints.get('max', 1000)
                    record[field_name] = round(random.uniform(min_val, max_val), 2)
                elif field_type == 'date':
                    start_date = constraints.get('start_date', '-1y')
                    end_date = constraints.get('end_date', 'now')
                    record[field_name] = self.fake.date_time_between(start_date=start_date, end_date=end_date)
                elif field_type == 'choice':
                    options = constraints.get('options', ['option1', 'option2'])
                    record[field_name] = random.choice(options)
                elif field_type == 'text':
                    max_chars = constraints.get('max_chars', 100)
                    record[field_name] = self.fake.text(max_nb_chars=max_chars)
                else:
                    record[field_name] = self.fake.word()
            
            records.append(record)
        
        return records
