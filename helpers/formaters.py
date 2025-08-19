def format_invoice(invoice: dict) -> str:
    """Format an invoice in a readable string."""
    return f"""
            Invoice ID: {invoice.get('id', 'Unknown')}
            Invoice no.: {invoice.get('number', 'Unknown')}
            Seller: {invoice.get('seller_name', 'Unknown')}
            Buyer: {invoice.get('buyer_name', 'Unknown')}
            Sell Date: {invoice.get('sell_date', 'Unknown')}
            Price net: {invoice.get('price_net', 'Unknown')}
            Price gross: {invoice.get('price_gross', 'Unknown')}
            """

def format_detailed_invoice(invoice: dict) -> str:
    """Format an invoice in a readable string."""

    if not invoice:
        return "No invoice data available."
    
    detailed_invoice = "## Invoice Details:\n"

    for key, item in invoice.items():
        detailed_invoice += f"- {key.replace('_', ' ').capitalize()}: {item}\n"

    return detailed_invoice

def format_client(client: dict) -> str:
    """Format a client in a readable string."""
    
    if not client:
        return "No client data available."
    
    client_info = f"## {client.get("name")} :\n"

    for key, item in client.items():
        client_info += f"- {key.replace('_', ' ').capitalize()}: {item}\n"

    return client_info + "\n"

def format_period_parameter(period: str, date_from: str = "", date_to: str = "") -> str:
    period_parameter = period
    if date_from and date_to:
        period_parameter = f"more&date_from={date_from}&date_to={date_to}"

    return period_parameter

def format_seller(seller: dict) -> str:
    """Format a seller in a readable string."""
    
    if not seller:
        return "No seller data available."
    
    seller_info = f"""
                    - Seller Name: {seller.get('name', '')}
                    - Seller Tax No: {seller.get('tax_no', '')}
                    - Seller Short Name: {seller.get('shortcut', '')}
                    """
    

    return seller_info + "\n"
