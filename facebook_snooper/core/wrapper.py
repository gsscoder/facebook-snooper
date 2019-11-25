from abc import abstractmethod


class BrowserWrapper:
    def open(self, browser, url):
        return browser.open(url)
    
    def submit_selected(self, browser):
        return browser.submit_selected()