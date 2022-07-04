import requests
from twocaptcha import TwoCaptcha
from vars import TWOCAPTCHA_KEY
import string
import random

solver = TwoCaptcha(TWOCAPTCHA_KEY)

SITE_KEY: str = "68CECE5D-F360-8653-CA80-3CF99353DDD2"


alphabets = list(string.ascii_letters)
digits = list(string.digits)
special_characters = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


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
        "county_code": "BY",
        "team_name": user_surname,
        "tos_version": 3,
        "team_num_users": 5,
        "account_info_type": "new",
        "billing_schedule": "yearly",
        "currency": "USD",
        "signup_type": "trial"

    })
    print(r.text)
    print(password)
    if r.text[0:3] == "err":
        if r.text[6:11] == "email":
            return "email_error"
        elif r.text[6:11] == "funca":
            return "funcaptcha_error"
    else:
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
    return True


if __name__ == '__main__':
    with open("orders.txt", "r", encoding="utf-8") as f:
        file_data: str = f.read()
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
    result_str: str = ""
    print("Writing data")
    for line in output_data:
        result_str += line["user_email"] + ":" + line["user_password"] + "\n"
    with open("registered.txt", "w", encoding="utf-8") as f:
        f.write(result_str)
    print("Finished!")
    exit()
