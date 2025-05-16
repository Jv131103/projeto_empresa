from bs4 import BeautifulSoup
from playwright.sync_api import Error, TimeoutError

from project.config_playwrite import SiteExtractor


class SaucedemoMarket(SiteExtractor):
    def __init__(self, url: str, headless: bool) -> None:
        super().__init__(url, headless)
        self.start()

    def close_site(self) -> None:
        self.close()

    def parse_users(self, content: str) -> dict[str, list[str]]:
        # Substituições para facilitar o parse
        content = content.replace("Accepted usernames are:", "usernames").replace("Password for all users:", "password")
        list_information = content.split()

        # Verifica se os termos estão presentes para evitar erro
        if "usernames" not in list_information or "password" not in list_information:
            raise ValueError("Formato da página inesperado.")

        index_user = list_information.index("usernames")
        index_password = list_information.index("password")

        return {
            "usernames": list_information[index_user + 1:index_password],
            "password": list_information[index_password + 1:]
        }

    def extract(self, selector: str) -> str:
        self.wait_for_element(selector)
        content = self.get_inner_text(selector)
        return content

    def login(self, username: str, password: str) -> None:
        self.wait_for_element(".login_logo")
        self.click_element("#user-name")
        self.input_fill("#user-name", username)
        self.wait_for(2)
        self.click_element("#password")
        self.input_fill("#password", password)
        self.wait_for(1)
        self.click_element("#login-button")

    def voltar_para_login(self):
        self.execute_js("window.history.back()")
        self.wait_for_element("#login-button")

    def is_valid_login(self) -> bool:
        self.wait_for(5)  # Espera um pouco antes de pegar o conteúdo
        content = self.get_content_html()
        soup = BeautifulSoup(content, "html5lib")
        h3_error = soup.find("h3", attrs={"data-test": "error"})
        return h3_error is None

    def safe_click(self, selector: str) -> bool:
        try:
            self.wait_for_element(selector)
            self.click_element(selector)
            return True
        except (TimeoutError, Error):
            return False

    def add_to_cart(self, product_id: str) -> bool:
        return self.safe_click(f'button[id="{product_id}"]')

    def remove_from_cart(self, product_id: str) -> bool:
        return self.safe_click(f'button[id="{product_id}"]')

    def sort_by_price(self, low_to_high: bool = True) -> bool:
        try:
            selector = ".product_sort_container"
            option_value = "lohi" if low_to_high else "hilo"
            self.wait_for_element(selector)
            self.select_option_element(selector, option_value)
            self.wait_for(4)
            return True
        except (TimeoutError, Error):
            return False

    def get_all_prices(self) -> list[float]:
        self.wait_for_element(".inventory_item_price")
        price_elements = self.query_all(".inventory_item_price")
        return [float(p.inner_text().replace("$", "")) for p in price_elements]

    def all_buttons(self) -> list[str]:
        # Pega os IDs dos botões para usar diretamente no add_to_cart
        all_buttons = self.query_all('button[id^="add-to-cart"]')
        return [btn.get_attribute("id") for btn in all_buttons if btn.get_attribute("id")]

    def qtd_numbers_cart_is_valid(self) -> bool:
        qtd_prices = len(self.get_all_prices())
        buttons = self.all_buttons()
        for btn in buttons:
            print(f"Adicionando ao carrinho: {btn}")
            self.add_to_cart(btn)
        self.wait_for_element('.shopping_cart_badge')
        cart = self.extract('.shopping_cart_badge')
        # cart vem como string, qtd_prices é int — converta para int para comparar
        try:
            cart_number = int(cart)
        except ValueError:
            cart_number = 0
        self.wait_for(4)
        return cart_number == qtd_prices

    def clear_cart(self):
        # Acesse carrinho
        self.page.click(".shopping_cart_link")
        # Remove todos os itens com limite de tentativas para evitar loop infinito
        max_attempts = 10
        attempt = 0
        while self.page.query_selector("button[id^='remove-']") and attempt < max_attempts:
            self.page.click("button[id^='remove-']")
            self.wait_for(1)
            attempt += 1

    def get_all_image_sources(self) -> list[str]:
        self.wait_for_element(".inventory_item_img img")
        image_elements = self.query_all(".inventory_item_img img")
        return [img.get_attribute("src") for img in image_elements]

    def has_duplicate_images(self) -> bool:
        sources = self.get_all_image_sources()
        return len(set(sources)) != len(sources)

    def has_dog_image(self) -> bool:
        sources = self.get_all_image_sources()
        self.wait_for(4)
        for src in sources:
            if "sl-404" in src or "dog" in src:
                return True
        return False


if __name__ == "__main__":
    site = SaucedemoMarket("https://www.saucedemo.com/", headless=False)

    # Extrai informaçõpes dos usuários de teste
    content = site.extract('.login_credentials_wrap-inner')
    users_passwords = site.parse_users(content)
    standard, locked, problem, perfomance, error, visual = users_passwords["usernames"]
    passwd = users_passwords["password"][0]

    # Faz o login no site usando usuário "problem"
    site.login(standard, passwd)

    # Verifica se login é válido
    response = site.is_valid_login()
    print("Login válido:", response)

    # Adiciona produto
    product_id = "add-to-cart-sauce-labs-backpack"
    print("Adicionar produto:", site.add_to_cart(product_id))

    # Remove produto
    product_id = "remove-sauce-labs-backpack"
    print("Remover produto:", site.remove_from_cart(product_id))

    print("Ordenar por preço crescente:", site.sort_by_price())  # Preço crescente
    print("Ordenar por preço decrescente:", site.sort_by_price(low_to_high=False))  # Preço decrescente

    prices = site.get_all_prices()
    print("Preços:", prices)

    # Verificar imagens
    print("Tem imagem do cachorro:", site.has_dog_image())
    print("Tem imagens duplicadas:", site.has_duplicate_images())

    # Verificar se itens estão sendo clicados e quantidade no carrinho está correta
    valid_cart = site.qtd_numbers_cart_is_valid()
    print("Quantidade no carrinho válida:", valid_cart)

    # Voltar ao login
    site.voltar_para_login()

    # Fecha o site
    site.close_site()
