import pytest

from project.saucedemo import SaucedemoMarket


@pytest.fixture(scope="module")
def site():
    # Inicializa a instância para todos os testes do módulo
    site = SaucedemoMarket("https://www.saucedemo.com/", headless=True)
    yield site
    site.close_site()


@pytest.mark.parametrize(
    "username_key, expected_valid",
    [
        ("standard", True),
        ("locked", False),
        ("problem", True),
        ("perfomance", True),
        ("error", True),
        ("visual", True),
    ]
)
def test_login(site, username_key, expected_valid):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    usernames = users_passwords["usernames"]
    passwords = users_passwords["password"]

    user_map = {
        "standard": 0,
        "locked": 1,
        "problem": 2,
        "perfomance": 3,
        "error": 4,
        "visual": 5
    }
    user = usernames[user_map[username_key]]
    passwd = passwords[0]

    site.login(user, passwd)
    is_valid = site.is_valid_login()

    assert is_valid == expected_valid, (
        f"Usuário '{username_key}' esperado login válido: {expected_valid}, "
        f"mas recebeu: {is_valid}"
    )

    site.voltar_para_login()


@pytest.mark.parametrize("product_id", [
    "add-to-cart-sauce-labs-backpack",
    "add-to-cart-sauce-labs-bike-light",
    "add-to-cart-sauce-labs-bolt-t-shirt"
])
def test_add_product(site, product_id):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user = users_passwords["usernames"][0]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    added = site.add_to_cart(product_id)
    assert added, f"Falhou ao adicionar produto {product_id}"

    site.wait_for(3)

    site.voltar_para_login()


@pytest.mark.parametrize("product_id", [
    "remove-sauce-labs-backpack",
    "remove-sauce-labs-bike-light",
    "remove-sauce-labs-bolt-t-shirt"
])
def test_remove_product(site, product_id):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user = users_passwords["usernames"][0]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    removed = site.remove_from_cart(product_id)
    assert removed, f"Falhou ao remover produto {product_id}"

    site.voltar_para_login()


def test_sort_prices_ascending(site):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user = users_passwords["usernames"][0]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    assert site.sort_by_price(True), "Falha ao ordenar preço crescente"
    prices = site.get_all_prices()
    assert prices == sorted(prices), "Preços não estão ordenados crescente"

    site.wait_for(3)

    site.voltar_para_login()


def test_sort_prices_descending(site):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user = users_passwords["usernames"][0]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    assert site.sort_by_price(False), "Falha ao ordenar preço decrescente"
    prices = site.get_all_prices()
    assert prices == sorted(prices, reverse=True), "Preços não estão ordenados decrescente"

    site.voltar_para_login()


def test_login_empty_fields(site):
    site.login("", "")
    assert not site.is_valid_login(), "Login deve falhar com campos vazios"
    site.voltar_para_login()


def test_login_wrong_password(site):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user = users_passwords["usernames"][0]
    wrong_passwd = "wrong_password"
    site.login(user, wrong_passwd)
    assert not site.is_valid_login(), "Login deve falhar com senha errada"
    site.voltar_para_login()


@pytest.mark.parametrize("username_key, expect_duplicates", [
    ("standard", False),
    ("locked", False),  # não chega a logar
    ("problem", True),
    ("perfomance", False),
    ("error", False),
    ("visual", False)
])
def test_duplicate_images_for_user(site, username_key, expect_duplicates):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user_map = {
        "standard": 0,
        "locked": 1,
        "problem": 2,
        "perfomance": 3,
        "error": 4,
        "visual": 5
    }
    user = users_passwords["usernames"][user_map[username_key]]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    try:
        if username_key == "locked":
            assert not site.is_valid_login(), f"Usuário {username_key} deveria continuar na página de login"
            return

        if expect_duplicates:
            assert site.has_duplicate_images(), f"Esperado imagens duplicadas para usuário {username_key}"
        else:
            assert not site.has_duplicate_images(), f"Duplicatas encontradas para usuário {username_key}"
    finally:
        site.voltar_para_login()


@pytest.mark.parametrize("username_key, expect_dog", [
    ("standard", False),
    ("locked", False),
    ("problem", True),
    ("perfomance", False),
    ("error", False),
    ("visual", True)
])
def test_dog_image_for_user(site, username_key, expect_dog):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user_map = {
        "standard": 0,
        "locked": 1,
        "problem": 2,
        "perfomance": 3,
        "error": 4,
        "visual": 5
    }
    user = users_passwords["usernames"][user_map[username_key]]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    try:
        if username_key == "locked":
            assert not site.is_valid_login(), f"Usuário {username_key} deveria continuar na página de login"
            return

        if expect_dog:
            assert site.has_dog_image(), f"Imagem do cão não encontrada para usuário {username_key}"
        else:
            assert not site.has_dog_image(), f"Imagem do cão **não deveria** aparecer para {username_key}"
    finally:
        site.voltar_para_login()


@pytest.mark.parametrize("username_key", ["standard", "problem", "perfomance"])
def test_cart_quantity_for_user(site, username_key):
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    user_map = {
        "standard": 0,
        "locked": 1,
        "problem": 2,
        "perfomance": 3,
        "error": 4,
        "visual": 5
    }
    user = users_passwords["usernames"][user_map[username_key]]
    passwd = users_passwords["password"][0]
    site.login(user, passwd)

    buttons = site.all_buttons()
    for btn in buttons:
        site.add_to_cart(btn)

    # Verifica a quantidade total no carrinho uma única vez
    assert site.qtd_numbers_cart_is_valid(), f"Quantidade inválida no carrinho para {username_key}"

    site.voltar_para_login()
