"""
Representa una compra pendiente.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ShoppingItem:

    resource: str

    amount: int

    priority: int = 0