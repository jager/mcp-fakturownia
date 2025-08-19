from attr import dataclass
from datetime import date, timedelta


@dataclass
class position:
    name: str
    total_price_gross: float
    quantity: int = 1
    tax: int = 0


@dataclass
class invoice:
    number: str | None
    client_id: str
    seller_name: str
    seller_tax_no: str
    issue_date: str
    sell_date: str
    payment_to: str
    positions: list[position]
    kind: str = "vat"
    

    def __attrs_post_init__(self):
        if not self.issue_date:
            self.issue_date = date.today().isoformat()

        if not self.sell_date:
            self.sell_date = date.today().isoformat()

        if not self.payment_to:
            self.payment_to = (date.today() + timedelta(days=7)).isoformat()

def create_new_invoice(client_id: str, seller_name: str, seller_tax_no: str, positions: list, sell_date: str = "", issue_date: str = "", payment_to: str = "", kind: str = "vat", number: str | None = None) -> invoice:
    """Create invoice."""
    return invoice(
        number=number,
        client_id=client_id,
        seller_name=seller_name,
        seller_tax_no=seller_tax_no,
        positions=[position(**pos) for pos in positions],
        sell_date=sell_date,
        issue_date=issue_date,
        payment_to=payment_to,
        kind=kind
    )