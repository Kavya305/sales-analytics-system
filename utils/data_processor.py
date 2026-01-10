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
