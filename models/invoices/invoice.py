from attr import dataclass
from datetime import date, timedelta


@dataclass
class position:
    name: str
    total_price_gross: float
    quantity: int = 1
    tax: str = "zw"


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
    exempt_tax_kind: str = ""
    

    def __attrs_post_init__(self):
        if not self.issue_date:
            self.issue_date = date.today().isoformat()

        if not self.sell_date:
            self.sell_date = date.today().isoformat()

        if not self.payment_to:
            self.payment_to = (date.today() + timedelta(days=7)).isoformat()

        if "zw" in [pos.tax for pos in self.positions]:
            self.exempt_tax_kind = "Zwolnienie ze względu na nieprzekroczenie 200 000 PLN obrotu (art. 113 ust 1 i 9 ustawy o VAT)"

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

def create_position(position_id: str, name: str = "", total_price_gross: float = 0.0, quantity: int = 1, tax: str = "zw") -> dict:
    """Create position."""
    position = { "id": position_id }

    if name:
        position["name"] = name

    if total_price_gross:
        position["total_price_gross"] = str(total_price_gross)

    if quantity:
        position["quantity"] = str(quantity)

    if tax:
        position["tax"] = tax

    return position