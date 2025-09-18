#!/usr/bin/env python3
"""
Data generation script for NimbusMegaMart data engineering exercise.
Generates sample JSON data for events, users, and items.
"""

import json
import random
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configuration
NUM_USERS = 1000
NUM_ITEMS = 200
NUM_EVENTS = 50000
START_DATE = datetime(2025, 8, 1)
END_DATE = datetime(2025, 8, 31)

# Sample data
COUNTRIES = ['US', 'CA', 'GB', 'DE', 'FR', 'JP', 'AU', 'BR', 'IN', 'CN']
CATEGORIES = ['electronics', 'clothing', 'books', 'home', 'sports', 'beauty', 'toys', 'food']
EVENT_TYPES = ['view', 'click', 'add_to_cart', 'purchase', 'remove_from_cart']

def generate_users() -> List[Dict[str, Any]]:
    """Generate sample user data."""
    users = []
    for i in range(1, NUM_USERS + 1):
        user = {
            'user_id': f'user_{i:06d}',
            'country': random.choice(COUNTRIES),
            'age': random.randint(18, 70),
            'gender': random.choice(['M', 'F', 'Other']),
            'registration_date': (START_DATE - timedelta(days=random.randint(0, 365))).isoformat()
        }
        users.append(user)
    return users

def generate_items() -> List[Dict[str, Any]]:
    """Generate sample item data."""
    items = []
    for i in range(1, NUM_ITEMS + 1):
        item = {
            'item_id': f'item_{i:06d}',
            'category': random.choice(CATEGORIES),
            'price': round(random.uniform(5.0, 500.0), 2),
            'brand': f'Brand_{random.randint(1, 50)}',
            'name': f'Product {i}'
        }
        items.append(item)
    return items

def generate_events(users: List[Dict], items: List[Dict]) -> List[Dict[str, Any]]:
    """Generate sample event data."""
    events = []
    user_ids = [u['user_id'] for u in users]
    item_ids = [i['item_id'] for i in items]
    
    for i in range(NUM_EVENTS):
        # Generate random timestamp within date range
        time_delta = END_DATE - START_DATE
        random_seconds = random.randint(0, int(time_delta.total_seconds()))
        event_time = START_DATE + timedelta(seconds=random_seconds)
        
        user_id = random.choice(user_ids)
        item_id = random.choice(item_ids)
        event_type = random.choice(EVENT_TYPES)
        
        # Find the item to get its price
        item = next(item for item in items if item['item_id'] == item_id)
        
        event = {
            'event_id': f'event_{i:08d}',
            'user_id': user_id,
            'item_id': item_id,
            'event_type': event_type,
            'ts': int(event_time.timestamp()),
            'props': {}
        }
        
        # Add properties based on event type
        if event_type == 'purchase':
            # Sometimes add some noise to price (including negative values for testing)
            price_multiplier = random.choice([1.0, 1.0, 1.0, 1.0, -0.1, 0.9, 1.1])
            event['props']['price'] = round(item['price'] * price_multiplier, 2)
        elif event_type == 'view':
            event['props']['duration'] = random.randint(1, 300)
        elif event_type == 'add_to_cart':
            event['props']['quantity'] = random.randint(1, 5)
        
        events.append(event)
    
    return events

def write_jsonl(data: List[Dict], filename: str):
    """Write data to JSON Lines format."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        for record in data:
            f.write(json.dumps(record) + '\n')

def main():
    """Generate all sample data files."""
    print("Generating sample data for NimbusMegaMart...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate and save users
    print(f"Generating {NUM_USERS} users...")
    users = generate_users()
    write_jsonl(users, 'data/users.jsonl')
    
    # Generate and save items
    print(f"Generating {NUM_ITEMS} items...")
    items = generate_items()
    write_jsonl(items, 'data/items.jsonl')
    
    # Generate and save events
    print(f"Generating {NUM_EVENTS} events...")
    events = generate_events(users, items)
    write_jsonl(events, 'data/events.jsonl')
    
    print("Data generation complete!")
    print(f"Files created:")
    print(f"  - data/users.jsonl ({len(users)} records)")
    print(f"  - data/items.jsonl ({len(items)} records)")
    print(f"  - data/events.jsonl ({len(events)} records)")

if __name__ == '__main__':
    main()