from config_playwrite import SiteExtractor


class SaucedemoMarket(SiteExtractor):
    def __init__(self, url: str, headless: bool) -> None:
        super().__init__(url, headless)
        self.start()

    def close_site(self) -> None:
        self.close()

    def parse_users(self, content: str) -> dict[str, list[str]]:
        content = content.replace("Accepted usernames are:", "usernames").replace("Password for all users:", "password")
        list_information = content.split()
        index_user = list_information.index("usernames")
        index_password = list_information.index("password")

        if "usernames" not in list_information or "password" not in list_information:
            raise ValueError("Formato da página inesperado.")

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


if __name__ == "__main__":
    site = SaucedemoMarket("https://www.saucedemo.com/", headless=False)
    content = site.extract('.login_credentials_wrap-inner')
    standard, locked, problem, perfomance, error, visual = site.parse_users(content)["usernames"]
    passwd = site.parse_users(content)["password"][0]
    site.login(standard, passwd)
    site.close_site()
