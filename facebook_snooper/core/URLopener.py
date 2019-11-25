from abc import abstractmethod


class URLopener:
    def open(self, browser, url):
        return browser.open(url)