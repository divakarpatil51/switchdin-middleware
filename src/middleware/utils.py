from decimal import Decimal


def watts_to_kilowatts(capacity: Decimal) -> Decimal:
    return Decimal(capacity / 1000)
