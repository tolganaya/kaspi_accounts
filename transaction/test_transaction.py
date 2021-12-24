from decimal import Decimal
from uuid import uuid4, UUID

import pytest
import json

from transaction.transaction import Transaction, CurrencyMismatchError


class TestTransaction:
    def test_transaction_create(self) -> None:
        transaction = Transaction(
            id_=uuid4(),
            currency="KZT",
            amount=Decimal(10),
        )
        assert isinstance(transaction, Transaction)
        assert transaction.amount == 10

        transaction2 = Transaction(
            id_=uuid4(),
            currency="KZT",
            amount=Decimal(5),
        )

        assert transaction2 < transaction

    def test_errors(self) -> None:
        transaction = Transaction(
            id_=uuid4(),
            currency="KZT",
            amount=Decimal(10),
        )

        transaction2 = Transaction(
            id_=uuid4(),
            currency="USD",
            amount=Decimal(5),
        )

        with pytest.raises(CurrencyMismatchError):
            assert transaction2 < transaction

    def test_json_import_export(self) -> None:
        transaction = Transaction.random()

        json_account = transaction.to_json()
        assert json.loads(json_account) == {
            "id": str(transaction.id_),
            "currency": transaction.currency,
            "amount": transaction.amount,
        }

    def test_account_from_json(self) -> None:
        test_json = '{"id": "a7cf405f-21ec-41b1-b22e-10298eb42510", "currency": "KZT", "amount": 10.0}'

        transaction = Transaction.from_json(test_json)
        assert isinstance(transaction, Transaction)
        assert transaction.id_ == UUID("a7cf405f-21ec-41b1-b22e-10298eb42510")
        assert transaction.amount == Decimal(10)
        assert transaction.currency == "KZT"

    def test_to_json_from_json(self) -> None:
        # Check all fields are serialized
        transaction = Transaction.random()
        transaction2 = Transaction.from_json(transaction.to_json())
        assert transaction2 == transaction