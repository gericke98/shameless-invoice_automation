# Invoice Extraction Automation

This script generates PDF invoices from Shopify order data using the Shopify API and the ReportLab library. The generated invoices include detailed customer information, order details, and company information.

## Prerequisites

- Python 3.6 or higher
- `requests` package
- `reportlab` package
- `python-dotenv` package

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gericke98/shameless-order_automation.git
   ```

## Configuration

Update the following variables in the script as needed:

- image_path: Logo of the company to be included in the invoice
- date_inicial: Start date for order filtering
- date_final: End date for order filtering
