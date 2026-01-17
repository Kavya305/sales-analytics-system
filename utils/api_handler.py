import requests


def fetch_all_products():
    """
    Task 3.1 (a)
    Fetches all products from DummyJSON API
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get('products', [])

        result = []
        for p in products:
            result.append({
                'id': p.get('id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'price': p.get('price'),
                'rating': p.get('rating')
            })

        print("Product fetch successful")
        return result

    except Exception as e:
        print("Product fetch failed")
        return []


def create_product_mapping(api_products):
    """
    Task 3.1 (b)
    Creates a mapping of product IDs to product info
    """

    product_mapping = {}

    for product in api_products:
        pid = product.get('id')

        if pid is not None:
            product_mapping[pid] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Task 3.2
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for tx in transactions:
        enriched = tx.copy()

        api_category = None
        api_brand = None
        api_rating = None
        api_match = False

        try:
            # Extract numeric product ID (P101 -> 101)
            product_id_str = tx.get('ProductID', '')
            numeric_id = int(''.join(filter(str.isdigit, product_id_str)))

            if numeric_id in product_mapping:
                product = product_mapping[numeric_id]
                api_category = product.get('category')
                api_brand = product.get('brand')
                api_rating = product.get('rating')
                api_match = True

        except Exception:
            api_match = False

        enriched['API_Category'] = api_category
        enriched['API_Brand'] = api_brand
        enriched['API_Rating'] = api_rating
        enriched['API_Match'] = api_match

        enriched_transactions.append(enriched)

    # Save to file as required
    save_enriched_data(enriched_transactions)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Helper function
    Saves enriched transactions back to file
    """

    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(header)

        for tx in enriched_transactions:
            row = [
                str(tx.get('TransactionID', '')),
                str(tx.get('Date', '')),
                str(tx.get('ProductID', '')),
                str(tx.get('ProductName', '')),
                str(tx.get('Quantity', '')),
                str(tx.get('UnitPrice', '')),
                str(tx.get('CustomerID', '')),
                str(tx.get('Region', '')),
                str(tx.get('API_Category', '')),
                str(tx.get('API_Brand', '')),
                str(tx.get('API_Rating', '')),
                str(tx.get('API_Match', ''))
            ]

            file.write('|'.join(row) + '\n')
