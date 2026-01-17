def calculate_total_revenue(transactions):
    """
    Task 2.1 (a)
    Calculates total revenue from all transactions
    """
    total = 0.0
    for tx in transactions:
        total += tx['Quantity'] * tx['UnitPrice']
    return total


def region_wise_sales(transactions):
    """
    Task 2.1 (b)
    Analyzes sales by region
    """

    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx['Region']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += revenue
        region_data[region]['transaction_count'] += 1

    # Add percentage and sort by total_sales desc
    sorted_regions = sorted(
        region_data.items(),
        key=lambda x: x[1]['total_sales'],
        reverse=True
    )

    result = {}
    for region, data in sorted_regions:
        percentage = (data['total_sales'] / total_revenue) * 100 if total_revenue else 0
        result[region] = {
            'total_sales': data['total_sales'],
            'transaction_count': data['transaction_count'],
            'percentage': round(percentage, 2)
        }

    return result


def top_selling_products(transactions, n=5):
    """
    Task 2.1 (c)
    Finds top n products by total quantity sold
    """

    product_data = {}

    for tx in transactions:
        name = tx['ProductName']
        qty = tx['Quantity']
        revenue = qty * tx['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]['quantity'],
        reverse=True
    )

    result = []
    for name, data in sorted_products[:n]:
        result.append((name, data['quantity'], data['revenue']))

    return result


def customer_analysis(transactions):
    """
    Task 2.1 (d)
    Analyzes customer purchase patterns
    """

    customer_data = {}

    for tx in transactions:
        cid = tx['CustomerID']
        revenue = tx['Quantity'] * tx['UnitPrice']
        product = tx['ProductName']

        if cid not in customer_data:
            customer_data[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }

        customer_data[cid]['total_spent'] += revenue
        customer_data[cid]['purchase_count'] += 1
        customer_data[cid]['products'].add(product)

    sorted_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]['total_spent'],
        reverse=True
    )

    result = {}
    for cid, data in sorted_customers:
        avg_order = data['total_spent'] / data['purchase_count']
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_order, 2),
            'products_bought': list(data['products'])
        }

    return result


def daily_sales_trend(transactions):
    """
    Task 2.2 (a)
    Analyzes sales trends by date
    """

    daily_data = {}

    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)

    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            'revenue': daily_data[date]['revenue'],
            'transaction_count': daily_data[date]['transaction_count'],
            'unique_customers': len(daily_data[date]['customers'])
        }

    return result


def find_peak_sales_day(transactions):
    """
    Task 2.2 (b)
    Identifies the date with highest revenue
    """

    daily_data = {}

    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1

    peak_date = max(daily_data.items(), key=lambda x: x[1]['revenue'])

    return (
        peak_date[0],
        peak_date[1]['revenue'],
        peak_date[1]['transaction_count']
    )


def low_performing_products(transactions, threshold=10):
    """
    Task 2.3 (a)
    Identifies products with low sales
    """

    product_data = {}

    for tx in transactions:
        name = tx['ProductName']
        qty = tx['Quantity']
        revenue = qty * tx['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    low_products = [
        (name, data['quantity'], data['revenue'])
        for name, data in product_data.items()
        if data['quantity'] < threshold
    ]

    low_products.sort(key=lambda x: x[1])

    return low_products
