from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time


def make_txt(names, new_prices, old_prices, category, date):
    str_for_file, counter = date + '\n', 1
    for i in range(len(names)):
        str_for_file += str(counter) + '. ' + names[i] + ' ' + new_prices[i] + ' ' + old_prices[i] + '\n\n'
        counter += 1
    filename = 'Silpo_' + category + '.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str_for_file)


def get_html(url, category):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    driver.maximize_window()
    try:
        driver.get(url=url)
        driver.find_elements(By.CLASS_NAME, "product-title")
        y = 500
        last_prod = 'test'
        while True:
            find_more_elements = driver.find_elements(By.CLASS_NAME, "product-title")
            time.sleep(0.25)
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 700
            if last_prod == find_more_elements[-1].text:
                l = driver.find_elements(By.TAG_NAME, "button")
                check = False
                for i in l:
                    if i.text == 'ПОКАЗАТИ ЩЕ':
                        action = ActionChains(driver)
                        action.move_to_element(i).click().perform()
                        time.sleep(1)
                        y += 500
                        check = True
                        break
                if check is False:
                    break
            else:
                last_prod = find_more_elements[-1].text

        name = driver.find_elements(By.CLASS_NAME, "product-title")
        new_price = driver.find_elements(By.CLASS_NAME, "current-integer")
        old_price = driver.find_elements(By.CLASS_NAME, "old-price")

        names, new_prices, old_prices = list(), list(), list()
        for i in range(len(new_price)):
            names.append(name[i].text)
            new_prices.append(new_price[i].text)
            old_prices.append((old_price[i]).text)

        date = (str(datetime.datetime.now())).split()
        make_txt(names, new_prices, old_prices, category, date[0])

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    SILPO = {
        'https://shop.silpo.ua/all-offers?filter_CATEGORY=(22)': 'alcohol',
        'https://shop.silpo.ua/all-offers?filter_CATEGORY=(316__277)': 'meat',
        'https://shop.silpo.ua/all-offers?filter_CATEGORY=(130)': 'sauce'
    }

    for link in SILPO:
        get_html(link, SILPO[link])


if __name__ == '__main__':
    main()
