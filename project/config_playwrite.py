from playwright.sync_api import sync_playwright
from time import sleep


class SiteExtractor:
    def __init__(self, url, headless=True):
        self.url = url
        self.headless = headless
        self.browser = None
        self.page = None

    def start(self):
        self.p = sync_playwright().start()
        self.browser = self.p.firefox.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.goto(self.url)

    def wait_for_element(self, selector):
        self.page.wait_for_selector(selector)

    def wait_for(self, time):
        sleep(time)

    def input_fill(self, selector, value, timeout=15000):
        self.page.fill(selector, value, timeout=timeout)

    def click_element(self, selector):
        self.page.click(selector)

    def get_inner_text(self, selector):
        return self.page.inner_text(selector)

    def close(self):
        self.browser.close()
        self.p.stop()


if __name__ == "__main__":
    extractor = SiteExtractor("https://www.saucedemo.com/", headless=True)
    extractor.start()
    extractor.wait_for_element(".login_credentials_wrap-inner")
    content = extractor.get_inner_text(".login_credentials_wrap-inner")
    extractor.close()
    print(content)
