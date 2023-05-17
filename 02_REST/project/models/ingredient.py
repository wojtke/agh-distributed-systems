from typing import Optional

from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    amount: Optional[float]
    unit: Optional[str]

    @classmethod
    def from_spoonacular(cls, ingredient: dict):
        return cls(
            name=ingredient["name"],
            amount=ingredient["measures"]["metric"]["amount"],
            unit=ingredient["measures"]["metric"]["unitShort"]
        )
