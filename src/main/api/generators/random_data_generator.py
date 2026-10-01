from random import uniform, randint


class RandomDataGenerator:

    # === ПОЗИТИВНЫЕ ЗНАЧЕНИЯ ===
    @staticmethod
    def valid_deposit_amount() -> float:
        """Слот под валидную сумму депозита"""
        return round(uniform(1000.00, 9000.00), 2)

    @staticmethod
    def valid_transfer_amount() -> float:
        """Слот под валидную сумму перевода"""
        return round(uniform(500.00, 2000.00), 2)

    @staticmethod
    def valid_credit_amount() -> int:
        """Слот под валидную сумму кредита"""
        return randint(5000, 15000)

    @staticmethod
    def valid_credit_term() -> int:
        """Слот под валидный срок кредита"""
        return randint(3, 24)

    # === НЕГАТИВНЫЕ ЗНАЧЕНИЯ ===
    @staticmethod
    def deposit_amount_negative() -> float:
        """Слот под невалидную (отрицательную) сумму депозита"""
        return round(uniform(-1000.00, -1.00), 2)

    @staticmethod
    def credit_amount_negative() -> int:
        """Слот под слишком низкую сумму кредита (ниже 5000)"""
        return randint(100, 4999)

    @staticmethod
    def repay_amount_negative(credit_amount: float) -> float:
        """Слот под частичную (неполную) сумму погашения кредита"""
        return round(credit_amount - 1000.00, 2)

    @staticmethod
    def transfer_amount_negative(initial_balance: float) -> float:
        """Слот под сумму перевода, превышающую баланс"""
        random_offset = round(uniform(500.00, 1000.00), 2)
        return round(initial_balance + random_offset, 2)
