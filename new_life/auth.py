from selenium import webdriver
from selenium.webdriver.common.by import By
from steam_totp import generate_twofactor_code_for_time
from auth_data import AuthData


def make_auth(login: str, password: str, shared_secret: str):
    driver = webdriver.Chrome()
    driver.get("https://skinout.gg/api/steam/login")

    driver.implicitly_wait(2)

    login_element = driver.find_element(By.XPATH,
                                "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input")
    password_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input")
    button_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button")
    login_element.send_keys(login)
    password_element.send_keys(password)
    button_element.click()

    driver.implicitly_wait(2)

    guard_code = generate_twofactor_code_for_time(shared_secret=shared_secret)
    guard_code_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/form/div/div[2]/div[1]/div/input")
    for index, guard_code_element in enumerate(guard_code_elements):
        guard_code_element.send_keys(guard_code[index])

    driver.implicitly_wait(2)

    button_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div/div[2]/div[2]/div/form/input[5]")
    button_element.click()

    token_element = driver.find_element(By.XPATH, "/html/body/div[1]/header/div[1]")
    token = token_element.get_attribute("token")
    phpsessid_cookie = driver.get_cookie("PHPSESSID")

    auth_data = AuthData(token, phpsessid_cookie["value"])
    driver.quit()
    return auth_data
