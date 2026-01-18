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
    barcode: Optional[str] = None  # EAN čárový kód pro ověření v nutričních databázích
    location: Optional[str] = None  # Lokace (např. "Valašské Meziříčí")
    unit_price: Optional[float] = None  # Cena za jednotku (např. Kč/kg)
    unit: Optional[str] = None  # Jednotka (kg, l, ks)
    
    def __str__(self):
        discount_info = f"{self.discount_percentage}% off" if self.discount_percentage else "Discount"
        return f"{self.name} - {self.discount_price} Kč ({discount_info}) at {self.store}"
    
    def is_valid_on_date(self, date: datetime) -> bool:
        """
        Zkontroluje, zda je produkt platný k danému datu.
        
        Args:
            date: Datum ke kontrole (datetime objekt)
            
        Returns:
            True pokud je produkt platný, False jinak
        """
        if self.valid_from and date < self.valid_from:
            return False
        if self.valid_until and date > self.valid_until:
            return False
        return True
