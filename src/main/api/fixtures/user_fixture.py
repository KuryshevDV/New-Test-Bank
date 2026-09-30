from random import randint

import pytest

from src.main.api.models.create_creditor_request import CreateCreditorRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.user_deposit_request import UserDepositRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_USER"
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_account_user_id(api_manager, create_user_request):
    create_account_response = api_manager.user_steps.create_account(create_user_request)
    return create_account_response.id

@pytest.fixture
def create_creditor_request(api_manager):
    creditor_request = RandomModelGenerator.generate(CreateUserRequest)
    creditor_request.role = "ROLE_USER"
    api_manager.admin_steps.create_user(creditor_request)
    return creditor_request

@pytest.fixture
def create_receiver_account_id(api_manager, create_creditor_request):
    create_account_response = api_manager.user_steps.create_account(create_creditor_request)
    return create_account_response.id

@pytest.fixture
def create_creditor_account_user_id(api_manager, create_creditor_request):
    create_account_response = api_manager.user_steps.create_account(create_creditor_request)
    return create_account_response.id

@pytest.fixture
def create_deposited_account(api_manager, create_user_request, create_account_user_id):
    deposit_account_request = UserDepositRequest(accountId=create_account_user_id, amount=randint(a=500000, b=700000)/100)
    user_deposited_account = api_manager.user_steps.user_deposit(create_user_request, deposit_account_request)
    return user_deposited_account

@pytest.fixture
def credit_account_request(create_creditor_account_user_id):
    credit_account_request = CreateCreditorRequest(accountId=create_creditor_account_user_id, amount=5000, termMonths=randint(a=6, b=24))
    return create_creditor_account_user_id

@pytest.fixture
def create_credit_user_request(api_manager):
    # Генерируем пользователя специально с кредитной ролью
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_account_id(api_manager, create_credit_user_request):
    """Создает счет для специального кредитного пользователя"""
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    return account_response.id


@pytest.fixture
def active_credit_data(api_manager, create_credit_user_request, create_credit_account_id):
    """Фикстура создаёт активный кредит на случайную валидную сумму"""
    from random import randint
    from src.main.api.models.create_creditor_request import CreateCreditorRequest

    # Генерируем случайную сумму кредита, убирая хардкод
    credit_amount = randint(5000, 15000)
    random_term = randint(3, 24)

    credit_payload = CreateCreditorRequest(
        accountId=create_credit_account_id,
        amount=credit_amount,
        termMonths=random_term
    )
    # Создаём кредит через шаги
    response = api_manager.user_steps.credit_request(create_credit_user_request, credit_payload)

    # Возвращаем creditId, accountId и РЕАЛЬНУЮ сумму созданного кредита третьим элементом!
    return response.creditId, create_credit_account_id, credit_amount



@pytest.fixture
def transfer_prepared_data(api_manager, create_user_request, create_account_user_id, create_receiver_account_id):
    """
    Фикстура готовит всё для перевода:
    1. Создает отправителя и получателя.
    2. Открывает обоим счета в банке.
    3. Пополняет счет отправителя на случайную валидную сумму.
    """
    from src.main.api.models.user_deposit_request import UserDepositRequest
    from random import uniform

    # Генерируем случайный начальный баланс в рамках лимитов (например, от 5000 до 9000)
    initial_balance = round(uniform(500.00, 9000.00), 2)

    deposit_payload = UserDepositRequest(accountId=create_account_user_id, amount=initial_balance)
    api_manager.user_steps.user_deposit(create_user_request, deposit_payload)

    # Возвращаем начальный баланс четвертым элементом в кортеже
    return create_user_request, create_account_user_id, create_receiver_account_id, initial_balance





