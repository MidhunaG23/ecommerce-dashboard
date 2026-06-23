"""
Generates a realistic sample e-commerce dataset so users can explore the
dashboard instantly without uploading their own file.
"""

import random
from datetime import datetime, timedelta
import pandas as pd


def generate_sample_data(n_rows: int = 300, seed: int = 42) -> pd.DataFrame:
    """Build a synthetic e-commerce sales dataset."""
    random.seed(seed)

    products = {
        "Electronics": ["Wireless Mouse", "Bluetooth Speaker", "Smartphone Case",
                         "LED Monitor", "Laptop Stand", "Power Bank", "USB-C Cable", "Smartwatch"],
        "Clothing": ["Men's T-Shirt", "Women's Jeans", "Winter Jacket",
                     "Cotton Saree", "Running Shoes", "Formal Shirt"],
        "Furniture": ["Office Chair", "Wooden Table", "Bookshelf", "Sofa Set", "Bed Frame"],
        "Grocery": ["Basmati Rice 5kg", "Cooking Oil 1L", "Organic Honey",
                    "Green Tea Pack", "Wheat Flour 10kg"],
        "Accessories": ["Leather Wallet", "Sunglasses", "Wrist Watch", "Backpack", "Hair Dryer"],
    }

    customers = [
        "Rahul Sharma", "Priya Verma", "Amit Singh", "Sneha Patel", "Vikram Rao",
        "Anita Desai", "Karan Mehta", "Pooja Iyer", "Rohan Gupta", "Neha Kapoor",
        "Arjun Nair", "Divya Joshi", "Manoj Kumar", "Kavita Reddy", "Suresh Pillai",
        "Ritu Agarwal", "Sandeep Yadav", "Meera Pillai", "Ajay Chauhan", "Swati Bhatt",
        "Vivek Malhotra", "Nidhi Saxena", "Rajesh Kulkarni", "Shreya Bansal",
        "Gaurav Khanna", "Pallavi Menon", "Naveen Reddy", "Aishwarya Rao",
        "Deepak Mishra", "Tanvi Shah",
    ]

    regions = ["North", "South", "East", "West", "Central"]
    all_products = [(p, c) for c, plist in products.items() for p in plist]

    start_date = datetime.today() - timedelta(days=365)
    rows = []
    for i in range(1, n_rows + 1):
        product, category = random.choice(all_products)
        customer = random.choice(customers)
        sales = round(random.uniform(500, 50000), 2)
        profit = round(sales * random.uniform(0.05, 0.30), 2)
        qty = random.randint(1, 10)
        region = random.choice(regions)
        order_date = start_date + timedelta(days=random.randint(0, 365))
        rows.append({
            "Order ID": f"ORD{1000 + i}",
            "Order Date": order_date.date(),
            "Product": product,
            "Category": category,
            "Customer Name": customer,
            "Sales": sales,
            "Profit": profit,
            "Quantity": qty,
            "Region": region,
        })

    return pd.DataFrame(rows)
