from attr import dataclass
"""
Data class representing a similar invoice request.

Attributes:
    copy_invoice_from (str): The identifier of the invoice to copy from.
    kind (str): The type or category of the similar invoice.
"""
@dataclass
class similar_invoice:
    copy_invoice_from: str
    kind: str
