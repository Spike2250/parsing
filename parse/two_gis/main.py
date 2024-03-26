from time import sleep
from urllib.parse import unquote
import pandas as pd
from selenium.webdriver.common.by import By

from parse.two_gis import paths
from parse.two_gis.paths import get_url
from parse.navig_parse import (
    get_driver,
    get_element_text,
    move_to_element,
    element_click
)


TABLE_COLUMNS = ['Название', 'Телефон', 'Адрес', 'Ссылка']
TABLE = {column: [] for column in TABLE_COLUMNS}


def parse(search_query, city='moscow'):
    url = get_url(search_query, city)
    driver = get_driver()
    driver.maximize_window()
    driver.get(url)
    element_click(driver, paths.main_banner)
    element_click(driver, paths.cookie_banner)
    count_all_items = int(get_element_text(driver, paths.items_count))
    pages = round(count_all_items / 12 + 0.5)

    for _ in range(pages):
        main_block = driver.find_element(By.XPATH, paths.main_block)
        count_items = len(main_block.find_elements(By.XPATH, 'div'))

        for item in range(1, count_items + 1):
            if main_block.find_element(
                    By.XPATH, f'div[{item}]').get_attribute('class'):
                continue
            item_clicked = element_click(main_block, f'div[{item}]/div/div[2]')
            if not item_clicked:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                element_click(main_block, f'div[{item}]/div/div[2]')

            title = get_element_text(driver, paths.title)
            phone_btn_clicked = element_click(driver, paths.phone_btn)
            phone = get_element_text(driver, paths.phone) if phone_btn_clicked else ''  # noqa: E501
            move_to_element(driver, main_block)
            link = unquote(driver.current_url)
            address = get_element_text(driver, paths.address)

            TABLE['Название'].append(title)
            TABLE['Телефон'].append(phone)
            TABLE['Адрес'].append(address)
            TABLE['Ссылка'].append(link)

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        element_click(driver, paths.next_page_btn)
        sleep(0.5)

    driver.quit()
    pd.DataFrame(TABLE).to_excel(f"{search_query}, {city}.xlsx")
