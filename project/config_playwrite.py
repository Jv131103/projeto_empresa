from time import sleep
from typing import Optional

from playwright.sync_api import (Browser, ElementHandle, Page, Playwright,
                                 sync_playwright)


class SiteExtractor:
    url: str
    headless: bool
    p: Optional[Playwright]
    browser: Optional[Browser]
    page: Optional[Page]

    def __init__(self, url: str, headless: bool = True) -> None:
        self.url = url
        self.headless = headless
        self.p = None
        self.browser = None
        self.page = None

    def start(self) -> None:
        self.p = sync_playwright().start()
        self.browser = self.p.firefox.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.goto(self.url)

    def wait_for_element(self, selector: str) -> None:
        assert self.page is not None, "Browser page is not initialized"
        self.page.wait_for_selector(selector)

    def wait_for(self, time: float) -> None:
        sleep(time)

    def input_fill(self, selector: str, value: str, timeout: int = 15000) -> None:
        assert self.page is not None, "Browser page is not initialized"
        self.page.fill(selector, value, timeout=timeout)

    def click_element(self, selector: str) -> None:
        assert self.page is not None, "Browser page is not initialized"
        self.page.click(selector)

    def select_option_element(self, selector: str, option_value: str) -> None:
        assert self.page is not None, "Browser page is not initialized"
        self.page.select_option(selector, option_value)

    def query_all(self, selector: str) -> list[ElementHandle]:
        return self.page.query_selector_all(selector)  # type: ignore

    def query_one(self, selector: str) -> Optional[ElementHandle]:
        return self.page.query_selector(selector)  # type: ignore

    def get_inner_text(self, selector: str) -> str:
        assert self.page is not None, "Browser page is not initialized"
        return self.page.inner_text(selector)

    def get_content_html(self) -> str:
        assert self.page is not None, "Browser page is not initialized"
        return self.page.content()

    def execute_js(self, script: str) -> None:
        assert self.page is not None, "Browser page is not initialized"
        self.page.evaluate(script)

    def close(self) -> None:
        if self.browser is not None:
            self.browser.close()
        if self.p is not None:
            self.p.stop()


if __name__ == "__main__":
    extractor = SiteExtractor("https://www.saucedemo.com/", headless=True)
    extractor.start()
    extractor.wait_for_element(".login_credentials_wrap-inner")
    content = extractor.get_inner_text(".login_credentials_wrap-inner")
    extractor.close()
    print(content)
