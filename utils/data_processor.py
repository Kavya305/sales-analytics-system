def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            transaction_id = parts[0]
            date = parts[1]
            product_id = parts[2]

            # Remove commas from ProductName
            product_name = parts[3].replace(',', '').strip()

            # Remove commas and convert numeric fields
            quantity = int(parts[4].replace(',', '').strip())
            unit_price = float(parts[5].replace(',', '').strip())

            customer_id = parts[6]
            region = parts[7]

            transactions.append({
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            })

        except ValueError:
            # Skip rows with conversion errors
            continue

    return transactions


# Data Validation and Filtering
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Returns:
    (valid_transactions, invalid_count, filter_summary)
    """

    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    # Validation 
    for tx in transactions:
        try:
            if tx['Quantity'] <= 0:
                raise ValueError
            if tx['UnitPrice'] <= 0:
                raise ValueError
            if not tx['TransactionID'].startswith('T'):
                raise ValueError
            if not tx['ProductID'].startswith('P'):
                raise ValueError
            if not tx['CustomerID'].startswith('C'):
                raise ValueError
            if not tx['Region']:
                raise ValueError

            valid_transactions.append(tx)

        except Exception:
            invalid_count += 1

    # Display available regions 
    regions = sorted({tx['Region'] for tx in valid_transactions})
    print("Available Regions:", regions)

    # Display transaction amount
    amounts = [tx['Quantity'] * tx['UnitPrice'] for tx in valid_transactions]
    min_tx_amount = min(amounts)
    max_tx_amount = max(amounts)
    print(f"Transaction Amount Range: {min_tx_amount} - {max_tx_amount}")

    filtered_by_region = 0
    filtered_by_amount = 0

    # Region
    if region:
        before = len(valid_transactions)
        valid_transactions = [
            tx for tx in valid_transactions if tx['Region'] == region
        ]
        filtered_by_region = before - len(valid_transactions)
        print(f"Records after region filter: {len(valid_transactions)}")

    # Amount 
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)
        filtered = []

        for tx in valid_transactions:
            amount = tx['Quantity'] * tx['UnitPrice']

            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue

            filtered.append(tx)

        valid_transactions = filtered
        filtered_by_amount = before - len(valid_transactions)
        print(f"Records after amount filter: {len(valid_transactions)}")

    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary

