import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
import json

class CurrencyMismatchError(ValueError):
    pass

@dataclass
class Transaction:
    id_: UUID
    #source_account: UUID
    #target_account: UUID
    #balance_brutto: Decimal
    #balance_netto: Decimal
    currency: str
    #status: str
    amount: Decimal

    def __lt__(self, other: "Transaction") -> bool:
        assert isinstance(other, Transaction)
        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.amount < other.amount

    def to_json(self) -> str:
        json_repr = {
            "id": str(self.id_),
            "currency": self.currency,
            "amount": float(self.amount),
        }
        return json.dumps(json_repr)

    @classmethod
    def from_json(cls, json_str: str) -> "Transaction":  # Factory
        obj = json.loads(json_str)
        if "currency" not in obj:
            raise ValueError("currency should be in json string!")
        if "amount" not in obj:
            raise ValueError("amount should be in json string!")
        if "id" not in obj:
            raise ValueError("id should be in json string!")

        return cls(
            id_=UUID(obj["id"]),
            currency=obj["currency"],
            amount=Decimal(obj["amount"]),
        )

    @classmethod
    def random(cls) -> "Transaction":  # Factory
        return cls(
            id_=uuid4(),
            currency="KZT",
            amount=Decimal(random.randint(1, 1000)),
        )