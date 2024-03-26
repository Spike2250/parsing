
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def get_driver():
    return webdriver.Chrome()


def get_element_text(driver: WebDriver, path: str) -> str:
    try:
        return driver.find_element(By.XPATH, path).text
    except NoSuchElementException:
        return ''


def move_to_element(driver: WebDriver,
                    element: WebElement | WebDriver) -> None:
    try:
        webdriver.ActionChains(driver).move_to_element(element).perform()
    except StaleElementReferenceException:
        pass


def element_click(driver: WebDriver | WebElement, path: str) -> bool:
    try:
        driver.find_element(By.XPATH, path).click()
        return True
    except Exception:
        return False
