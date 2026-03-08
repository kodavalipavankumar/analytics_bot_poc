from __future__ import annotations

import os
import random
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / '.env')

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://analytics_user:analytics_password@localhost:3306/analytics_poc',
)

REGIONS = ['North', 'South', 'East', 'West']
CATEGORIES = {
    'Furniture': ['Sofa', 'Dining Table', 'Chair', 'Bed'],
    'Electronics': ['Laptop', 'TV', 'Speaker', 'Phone'],
    'Appliances': ['Refrigerator', 'Microwave', 'Washer', 'Dryer'],
    'Decor': ['Lamp', 'Rug', 'Mirror', 'Curtains'],
}
SEGMENTS = ['Consumer', 'Corporate', 'Home Office']


def daterange(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def main() -> None:
    engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        order_id VARCHAR(50) NOT NULL,
        order_date DATE NOT NULL,
        region VARCHAR(50) NOT NULL,
        category VARCHAR(50) NOT NULL,
        product_name VARCHAR(100) NOT NULL,
        units_sold INT NOT NULL,
        sales_amount DECIMAL(12,2) NOT NULL,
        customer_segment VARCHAR(50) NOT NULL,
        INDEX idx_sales_order_date (order_date),
        INDEX idx_sales_region (region),
        INDEX idx_sales_category (category),
        INDEX idx_sales_product_name (product_name)
    ) ENGINE=InnoDB;
    """

    insert_sql = text(
        """
        INSERT INTO sales (
            order_id,
            order_date,
            region,
            category,
            product_name,
            units_sold,
            sales_amount,
            customer_segment
        ) VALUES (
            :order_id,
            :order_date,
            :region,
            :category,
            :product_name,
            :units_sold,
            :sales_amount,
            :customer_segment
        )
        """
    )

    rows: list[dict] = []
    rng = random.Random(42)
    order_num = 10000

    for d in daterange(date(2024, 1, 1), date(2025, 12, 31)):
        orders_today = rng.randint(4, 12)
        for _ in range(orders_today):
            region = rng.choice(REGIONS)
            category = rng.choice(list(CATEGORIES.keys()))
            product_name = rng.choice(CATEGORIES[category])
            units_sold = rng.randint(1, 8)
            unit_price = rng.uniform(40, 1800)
            sales_amount = round(units_sold * unit_price, 2)
            segment = rng.choice(SEGMENTS)
            rows.append(
                {
                    'order_id': f'ORD-{order_num}',
                    'order_date': d.isoformat(),
                    'region': region,
                    'category': category,
                    'product_name': product_name,
                    'units_sold': units_sold,
                    'sales_amount': sales_amount,
                    'customer_segment': segment,
                }
            )
            order_num += 1

    with engine.begin() as conn:
        conn.execute(text('DROP TABLE IF EXISTS sales'))
        conn.execute(text(create_table_sql))
        conn.execute(insert_sql, rows)

    print('Seeded MySQL demo database successfully.')
    print(f'DATABASE_URL={DATABASE_URL}')


if __name__ == '__main__':
    main()
