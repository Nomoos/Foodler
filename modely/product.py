"""
Datové modely pro produkty a slevy
Tento modul obsahuje pouze datové třídy (Single Responsibility Principle)
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """Reprezentuje produkt s informacemi o slevě."""
    name: str
    original_price: Optional[float]
    discount_price: float
    discount_percentage: Optional[float]
    store: str
    valid_from: Optional[datetime]
    valid_until: Optional[datetime]
    image_url: Optional[str]
    product_url: Optional[str]
    category: Optional[str]
    
    def __str__(self):
        discount_info = f"{self.discount_percentage}% off" if self.discount_percentage else "Discount"
        return f"{self.name} - {self.discount_price} Kč ({discount_info}) at {self.store}"
