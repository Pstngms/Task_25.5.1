import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


@pytest.fixture(autouse=True)
def testing():
    # Переходим на страницу авторизации
    driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    yield

    driver.quit()


def test_pet_cards():
    driver.implicitly_wait(10)
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    driver.implicitly_wait(10)
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    driver.implicitly_wait(10)
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_user_pet_table():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()

    pet_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    pet_count = int(pet_count.text.split('\n')[1].split(' ')[1])

    pet_photos = 0
    pet_names = []
    pet_breed = []
    pet_ages = []

    for i in range(pet_count):

        current_name = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr/td[1]")))[i].text
        current_breed = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr/td[2]")))[i].text
        current_age = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr/td[3]")))[i].text

        assert current_name not in pet_names
        assert current_name not in pet_names and current_breed not in pet_breed and current_age not in pet_ages

        pet_names.append(current_name)
        pet_breed.append(current_breed)
        pet_ages.append(current_age)

        if WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tr/th/img"))).get_attribute('src') != '':
            pet_photos += 1

    assert len(WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr")))) == pet_count
    assert pet_photos >= pet_count / 2
    assert '' not in pet_names
    assert '' not in pet_breed
    assert '' not in pet_ages
