import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from helpers import format_detailed_invoice, format_invoice, format_period_parameter, format_client, get_request, post_request, format_seller, put_request
from helpers.filters import filter_clients_by_name
from helpers.serialize import to_dict
from models import similar_invoice, create_new_invoice, position, invoice
from models.invoices.invoice import create_position

load_dotenv()

mcp = FastMCP("fakturownia")

API_BASE = os.getenv("API_BASE", "https://localhost")
API_TOKEN = os.getenv("API_TOKEN", "")
USER_AGENT = os.getenv("USER_AGENT", "fakturownia-app/1.0")

@mcp.tool()
async def get_invoices(period: str = "this_month", page: str = "1", per_page: str = "25", date_from: str = "", date_to: str = "") -> str:
    """Get invoices from the Fakturovnia API.
    
    - more (tutaj trzeba jeszcze dostarczyć dodatkowe parametry date_from (np. "2018-12-16") i date_to (np. "2018-12-21"))

    Args:
        period: The period to fetch alerts for (default: "this_month")
        page: Page number for pagination (default: "1")
        per_page: Number of results per page (default: "25")
        date_from: Start date for the period (optional)
        date_to: End date for the period (optional)

    Allowed periods:
        - last_12_months
        - this_month
        - last_30_days
        - last_month
        - this_year
        - last_year
        - all
    """
    period_parameter = format_period_parameter(period, date_from, date_to)
    url = f"{API_BASE}/invoices.json?period={period_parameter}&page={page}&per_page={per_page}&api_token={API_TOKEN}"
    data = await get_request(url, user_agent=USER_AGENT)

    if not data or len(data) == 0:
        return "Unable to fetch invoices or no invoices found."

    invoices = [format_invoice(invoice) for invoice in data]
    return "\n---\n".join(invoices)

@mcp.tool()
async def get_invoices_by_client_id(client_id: str = "") -> str:
    """Get invoices of given client from the Fakturovnia API.

    Args:
        period: The period to fetch alerts for (default: "this_month")
        page: Page number for pagination (default: "1")
        per_page: Number of results per page (default: "25")
    """

    url = f"{API_BASE}/invoices.json?client_id={client_id}&api_token={API_TOKEN}"
    data = await get_request(url, user_agent=USER_AGENT)

    if not data or len(data) == 0:
        return "Unable to fetch invoices or no invoices found."

    invoices = [format_invoice(invoice) for invoice in data]
    return "\n---\n".join(invoices)

@mcp.tool()
async def get_invoice(invoice_id: str) -> str:
    """Get a specific invoice by ID from the Fakturovnia API.

    Args:
        invoice_id: The ID of the invoice to fetch.
    """

    url = f"{API_BASE}/invoices/{invoice_id}.json?api_token={API_TOKEN}"
    data = await get_request(url, user_agent=USER_AGENT)

    if not data:
        return "Unable to fetch invoice or invoice not found."

    return format_detailed_invoice(data)

@mcp.tool()
async def find_clients_by_name(name: str = "") -> str:
    """Find clients by name in the Fakturovnia API.
    Args:
        name: The name of the client to search for. If empty, all clients will be returned.
    """

    url = f"{API_BASE}/clients.json?api_token={API_TOKEN}"
    data = await get_request(url, user_agent=USER_AGENT)

    if not data or len(data) == 0:
        return f"No clients found for given name: {name}."

    filtered_clients = filter_clients_by_name(list(data), name)
    clients = [format_client(client) for client in filtered_clients]
    return "\n---\n".join(clients)

@mcp.tool()
async def create_invoice_based_on_other_invoice(similar_invoice_id: str, kind: str = "vat") -> str:
    """Create a new invoice in the Fakturovnia API based on similar invoice.

    Args:
        similar_invoice_id: An identifier of similar invoice.
        kind: The type or category of the similar invoice (default: "vat").
    """
    invoice = similar_invoice(copy_invoice_from=similar_invoice_id, kind=kind)
    data = { "api_token": API_TOKEN, "invoice": invoice.__dict__ }
    url = f"{API_BASE}/invoices.json"
    response = await post_request(url, data, user_agent=USER_AGENT)

    if not response:
        return "Unable to create invoice."

    return f"Created successfully invoice based on similar invoice: {similar_invoice_id}."

@mcp.tool()
async def find_all_sellers() -> str:
    """Find all sellers in the Fakturovnia API."""
    url = f"{API_BASE}/departments.json?api_token={API_TOKEN}"
    data = await get_request(url, user_agent=USER_AGENT)

    if not data or len(data) == 0:
        return "No sellers found."

    sellers = [format_seller(seller) for seller in data]
    return "\n".join(sellers)

@mcp.tool()
async def create_invoice(client_id: str, positions: list, seller_name: str, seller_tax_no: str, sell_date: str = "", issue_date: str = "", payment_to: str = "", kind: str = "vat") -> str:
    """Create a new invoice in the Fakturovnia API.

    Args:
        client_id: The ID of the client for whom the invoice is created.
        positions: A list of positions to include in the invoice. Each position: name, total_price_gross, quantity (default: 1), tax (default: 0). 
        seller_name: The name of the seller.
        seller_tax_no: The tax number of the seller.
        sell_date: The date of sale (optional).
        issue_date: The date of issue (optional).
        payment_to: The payment due date (optional).
        kind: The type or category of the invoice (default: "vat").
    """
    if not client_id or not positions:
        return "Client ID and positions are required to create an invoice."
    
    invoice = create_new_invoice(
        client_id=client_id,
        positions=positions,
        sell_date=sell_date,
        issue_date=issue_date,
        payment_to=payment_to,
        kind=kind,
        seller_name=seller_name,
        seller_tax_no=seller_tax_no
    )

    data = {
        "api_token": API_TOKEN,
        "invoice": to_dict(invoice)
    }
    url = f"{API_BASE}/invoices.json"
    response = await post_request(url, data, user_agent=USER_AGENT)

    if not response:
        return "Unable to create invoice."

    return f"Invoice created successfully with ID: {response.get('id', 'Unknown')}."

@mcp.tool()
async def modify_position_on_invoice(invoice_id: str, position_id: str, name: str = "", total_price_gross: float = 0.0, quantity: int = 1, tax: int = 0) -> str:
    """Modify a position on an existing invoice in the Fakturovnia API.

    Args:
        invoice_id: The ID of the invoice to modify.
        position_id: The ID of the position to modify.
        name: The name of the position (optional).
        total_price_gross: The total price gross of the position (optional).
        quantity: The quantity of the position (default: 1).
        tax: The tax rate for the position (default: 0).
    """
    position = create_position(
        position_id=position_id,
        name=name,
        total_price_gross=total_price_gross,
        quantity=quantity,
        tax=tax
    )
    url = f"{API_BASE}/invoices/{invoice_id}.json?api_token={API_TOKEN}"
    data = {
        "api_token": API_TOKEN,
        "invoice": {
            "positions": [position]
        }
    }
    response = await put_request(url, data, user_agent=USER_AGENT)

    if not response:
        return "Unable to modify position on invoice."

    return f"Position modified successfully on invoice with ID: {invoice_id}."

if __name__ == "__main__":
    mcp.run(transport='stdio')


