from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Task 4.1
    Generates a comprehensive formatted text report
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    # ---------- OVERALL SUMMARY ----------
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_records if total_records else 0

    dates = [tx['Date'] for tx in transactions]
    date_range = f"{min(dates)} to {max(dates)}"

    # ---------- REGION PERFORMANCE ----------
    region_stats = region_wise_sales(transactions)

    # ---------- TOP PRODUCTS & CUSTOMERS ----------
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    top_customers = list(customers.items())[:5]

    # ---------- DAILY TRENDS ----------
    daily_trends = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)

    # ---------- PRODUCT PERFORMANCE ----------
    low_products = low_performing_products(transactions)

    # ---------- API ENRICHMENT SUMMARY ----------
    enriched_count = sum(1 for tx in enriched_transactions if tx.get('API_Match'))
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0
    failed_products = sorted({
        tx['ProductName']
        for tx in enriched_transactions
        if not tx.get('API_Match')
    })

    # ---------- WRITE REPORT ----------
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_records}\n")
        f.write("=" * 50 + "\n\n")

        # 1. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_records}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        # 2. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions'}\n")
        for region, data in region_stats.items():
            f.write(
                f"{region:<10}"
                f"₹{data['total_sales']:,.2f}  "
                f"{data['percentage']:<12}%"
                f"{data['transaction_count']}\n"
            )
        f.write("\n")

        # 3. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty Sold':<12}{'Revenue'}\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<6}{name:<20}{qty:<12}₹{rev:,.2f}\n")
        f.write("\n")

        # 4. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<12}{'Total Spent':<15}{'Orders'}\n")
        for i, (cid, data) in enumerate(top_customers, 1):
            f.write(
                f"{i:<6}{cid:<12}"
                f"₹{data['total_spent']:,.2f}  "
                f"{data['purchase_count']}\n"
            )
        f.write("\n")

        # 5. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<8}{'Customers'}\n")
        for date, data in daily_trends.items():
            f.write(
                f"{date:<12}"
                f"₹{data['revenue']:,.2f}  "
                f"{data['transaction_count']:<8}"
                f"{data['unique_customers']}\n"
            )
        f.write("\n")

        # 6. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Best Selling Day: {peak_day[0]} (₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                f.write(f"- {name}: Qty {qty}, Revenue ₹{rev:,.2f}\n")
        else:
            f.write("No low performing products found\n")
        f.write("\n")

        # 7. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products Not Enriched:\n")
        for p in failed_products:
            f.write(f"- {p}\n")
