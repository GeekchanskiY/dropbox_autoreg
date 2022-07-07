import time

import requests
from twocaptcha import TwoCaptcha
import string
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

solver = TwoCaptcha("KEY")

driver = webdriver.Chrome(executable_path="chromedriver.exe")

SITE_KEY: str = "68CECE5D-F360-8653-CA80-3CF99353DDD2"

alphabets = list(string.ascii_letters)
digits = list(string.digits)
special_characters = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def login_to_dropbox(driver: webdriver, login: str, password: str, team_name: str):
    driver.get("https://www.dropbox.com/login")
    time.sleep(5)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    inputs[0].send_keys(login)
    inputs[1].send_keys(password)
    driver.find_element(By.CLASS_NAME, "signin-button").click()
    time.sleep(10)
    driver.get("https://www.dropbox.com/business/try?sku=std")
    time.sleep(7)
    driver.find_element(By.ID, "team_name").send_keys(team_name)
    driver.find_element(By.CLASS_NAME, "input__checkbox").click()
    driver.find_element(By.CLASS_NAME, "confirm-button").click()
    driver.get("https://www.dropbox.com/home")
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "dig-Avatar").click()
    time.sleep(0.5)
    driver.find_elements(By.CLASS_NAME, "dig-Menu-row-title")[-2].click()


def generate_random_password() -> str:
    """
        Generates random password
    Return:
        (str) - password
    """
    length = 12

    alphabets_count = 4
    digits_count = 4
    special_characters_count = 4

    characters_count = alphabets_count + digits_count + special_characters_count

    password = []

    for i in range(alphabets_count):
        password.append(random.choice(alphabets))

    for i in range(digits_count):
        password.append(random.choice(digits))

    for i in range(special_characters_count):
        password.append(random.choice(special_characters))

    if characters_count < length:
        random.shuffle(characters)
        for i in range(length - characters_count):
            password.append(random.choice(characters))

    random.shuffle(password)

    return " ".join(map(str, password)).replace(" ", "")


def register(funcapcha_response: str, name, surname, email, password) -> str:
    s: requests.Session = requests.session()
    s.get("https://www.dropbox.com/register")
    t: str = s.cookies["t"]
    r = s.post("https://www.dropbox.com/checkout/create_user", data={
        "fname": name,
        "lname": surname,
        "email": email,
        "tos_agree": True,
        "password": password,
        "funcaptcha-response": funcapcha_response,
        "t": t,
        "is_xhr": True,
        "tracking_params": {},
        "signup_url": "https://www.dropbox.com/business/try",
        "schedule_id": 2,
        'signup_tag': 'team',
        "signup_data": "",
        "birthdate_ts": "",
        "county_code": "US",
        "team_name": surname,
        "tos_version": 3,
        "team_num_users": 5,
        "account_info_type": "new",
        "billing_schedule": "yearly",
        "currency": "USD",
        "signup_type": "trial"

    })

    if r.text.find("Too many attempts. Please try later") != -1:
        print("Too many attempts. Waiting 10 min")

        # Sleep if too many attempts error
        time.sleep(600)

        return register(funcapcha_response, name, surname, email, password)
    print(password)
    if r.text[0:3] == "err":
        if r.text[6:11] == "email":
            return "email_error"
        elif r.text[6:11] == "funca":
            return "funcaptcha_error"
    else:
        try:
            login_to_dropbox(driver, login=email, password=password, team_name=surname)
        except Exception as e:
            print(str(e))
            return "error"
        return "success"


def main(name, surname, email, password, recursion) -> bool:
    print(f"attempt {recursion}")
    if recursion == 5:
        return False
    try:
        res = solver.funcaptcha(
            sitekey=SITE_KEY,
            url="https://www.dropbox.com/business/try"
        )
    except Exception as e:
        print(str(e))
        m = main(name, surname, email, password, recursion + 1)
        if not m:
            return False
        return False

    reg = register(res["code"], name, surname, email, password)
    if reg == "funcaptcha_error":
        solver.report(res["captchaId"], False)
        m = main(name, surname, email, password, recursion+1)
        if not m:
            return False
    else:
        solver.report(res["captchaId"], True)
    if reg == "email_error":
        return False
    if reg == "error":
        return False
    return True


if __name__ == '__main__':

    try:
        with open("orders.txt", "r", encoding="utf-8") as f:
            file_data: str = f.read()
    except Exception as e:
        input("File not found")

    output_data: list[dict] = []

    for line in file_data.split("\n"):
        line_data: list[str] = line.split(":")
        user_email: str = line_data[0]
        user_name: str = line_data[1]
        user_surname: str = line_data[2]
        user_password: str = generate_random_password()
        print(f"Registering {user_name}")
        registered = main(email=user_email, name=user_name, surname=user_surname, password=user_password, recursion=1)

        if registered:
            output_data.append(
                {
                    "user_name": user_name,
                    "user_surname": user_surname,
                    "user_password": user_password,
                    "user_email": user_email
                }
            )
            print("registered")

            # Sleep between users
            time.sleep(60)

    result_str: str = ""
    print("Writing data")
    for line in output_data:
        result_str += line["user_email"] + ":" + line["user_password"] + "\n"
    with open("registered.txt", "w", encoding="utf-8") as f:
        f.write(result_str)
    print("Finished!")
    exit()