from random import uniform, randint
import pytest

from src.main.api.models.create_creditor_request import CreateCreditorRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.user_deposit_request import UserDepositRequest
from src.main.api.models.user_transfer_request import UserTransferRequest
from src.main.api.models.create_repay_request import CreateRepayRequest


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
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_account_id(api_manager, create_credit_user_request):
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    return account_response.id


@pytest.fixture
def active_credit_data(api_manager, create_credit_user_request, create_credit_account_id):
    """Фикстура создаёт активный кредит, используя RandomModelGenerator и валидные лимиты"""
    from random import randint

    credit_payload = RandomModelGenerator.generate(CreateCreditorRequest)
    credit_payload.accountId = create_credit_account_id

    # ПРИНУДИТЕЛЬНО РАМКИ БИЗНЕС-ЛОГИКИ БЭКЕНДА:
    credit_payload.amount = randint(5000, 15000)  # Лимит бэкенда: от 5000 до 15000
    credit_payload.termMonths = randint(3, 24)  # Лимит бэкенда: от 1 до 60

    response = api_manager.user_steps.credit_request(create_credit_user_request, credit_payload)
    return response.creditId, create_credit_account_id, credit_payload.amount


@pytest.fixture
def transfer_prepared_data(api_manager, create_user_request, create_account_user_id, create_receiver_account_id):
    """Фикстура готовит данные для перевода и начисляет валидный начальный баланс"""
    deposit_payload = RandomModelGenerator.generate(UserDepositRequest)
    deposit_payload.accountId = create_account_user_id
    deposit_payload.amount = round(uniform(5000.00, 8000.00), 2)  # Корректируем на валидный депозит

    api_manager.user_steps.user_deposit(create_user_request, deposit_payload)
    return create_user_request, create_account_user_id, create_receiver_account_id, deposit_payload.amount



# =====================================================================
# СЛОТЫ МОДЕЛЕЙ ДЛЯ ТЕСТОВ (ПОЗИТИВНЫЕ И НЕГАТИВНЫЕ)
# =====================================================================

# --- ДЕПОЗИТ ---
@pytest.fixture
def valid_deposit_request(create_account_user_id):
    """Позитивный слот: генерируем модель и корректируем сумму под лимит 1000-9000"""
    deposit_payload = RandomModelGenerator.generate(UserDepositRequest)
    deposit_payload.accountId = create_account_user_id
    deposit_payload.amount = round(uniform(1000.00, 9000.00), 2)  # Гарантированный лимит бэкенда
    return deposit_payload


@pytest.fixture
def invalid_deposit_request(create_account_user_id):
    """Негативный слот: объект депозита с умышленно отрицательной суммой"""
    deposit_payload = RandomModelGenerator.generate(UserDepositRequest)
    deposit_payload.accountId = create_account_user_id
    deposit_payload.amount = round(uniform(-1000.00, -1.00), 2)
    return deposit_payload


# --- ПЕРЕВОД ---
@pytest.fixture
def valid_transfer_request(transfer_prepared_data):
    """Позитивный слот: готовый объект перевода в рамках доступного баланса"""
    _, sender_account_id, receiver_account_id, initial_balance = transfer_prepared_data

    transfer_payload = RandomModelGenerator.generate(UserTransferRequest)
    transfer_payload.fromAccountId = sender_account_id
    transfer_payload.toAccountId = receiver_account_id
    # Сумма перевода должна быть валидной (от 500 до 10000) и не превышать баланс
    min_amount = max(500.00, initial_balance / 4)
    max_amount = min(10000.00, initial_balance / 2)
    transfer_payload.amount = round(uniform(min_amount, max_amount), 2)
    return transfer_payload


@pytest.fixture
def invalid_transfer_request(transfer_prepared_data):
    """Негативный слот: объект перевода на сумму, заведомо превышающую баланс"""
    _, sender_account_id, receiver_account_id, initial_balance = transfer_prepared_data

    transfer_payload = RandomModelGenerator.generate(UserTransferRequest)
    transfer_payload.fromAccountId = sender_account_id
    transfer_payload.toAccountId = receiver_account_id
    # Сумма больше баланса, но строго в рамках верхнего лимита (до 10000.00)
    transfer_payload.amount = round(min(9500.00, initial_balance + uniform(500.00, 1000.00)), 2)
    return transfer_payload


# --- ЗАПРОС КРЕДИТА ---
@pytest.fixture
def valid_credit_request(create_credit_account_id):
    """Позитивный слот: генерируем кредит и корректируем под лимиты бэкенда"""
    credit_payload = RandomModelGenerator.generate(CreateCreditorRequest)
    credit_payload.accountId = create_credit_account_id
    credit_payload.amount = randint(5000, 15000)  # Лимит: от 5000 до 15000
    credit_payload.termMonths = randint(3, 24)  # Лимит: от 1 до 60 месяцев
    return credit_payload


@pytest.fixture
def invalid_credit_request(create_credit_account_id):
    """Негативный слот: сумма ниже лимита бэкенда (меньше 5000)"""
    credit_payload = RandomModelGenerator.generate(CreateCreditorRequest)
    credit_payload.accountId = create_credit_account_id
    credit_payload.amount = randint(100, 4999)
    credit_payload.termMonths = 12
    return credit_payload


# --- ПОГАШЕНИЕ КРЕДИТА ---
@pytest.fixture
def valid_repay_request(active_credit_data):
    """Позитивный слот: готовый объект полного погашения кредита"""
    credit_id, account_id, credit_amount = active_credit_data

    repay_payload = RandomModelGenerator.generate(CreateRepayRequest)
    repay_payload.creditId = credit_id
    repay_payload.accountId = account_id
    repay_payload.amount = credit_amount
    return repay_payload


@pytest.fixture
def invalid_repay_request(active_credit_data):
    """Негативный слот: частичное погашение долга"""
    credit_id, account_id, credit_amount = active_credit_data

    repay_payload = RandomModelGenerator.generate(CreateRepayRequest)
    repay_payload.creditId = credit_id
    repay_payload.accountId = account_id
    repay_payload.amount = round(credit_amount - 1000)
    return repay_payload
