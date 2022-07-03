import requests
from twocaptcha import TwoCaptcha
from vars import TWOCAPTCHA_KEY

solver = TwoCaptcha(TWOCAPTCHA_KEY)

SITE_KEY: str = "68CECE5D-F360-8653-CA80-3CF99353DDD2"


def register(funcapcha_response: str,) -> str:
    s: requests.Session = requests.session()
    s.get("https://www.dropbox.com/register")
    t: str = s.cookies["t"]
    r = s.post("https://www.dropbox.com/ajax_register", data={
        "fname": "Dimka",
        "lname": "Nevidimka",
        "email": "ufdgoisdyuiozyuqtazxcveuigfhjkunbzvkmcnlk@mail.ru",
        "tos_agree": True,
        "password": "zxcvbzZOIUFSzxcmnvbmzx",
        "funcaptcha-response": funcapcha_response,
        "t": t,
        "is_xhr": True,
        "tracking_params": {},
        "signup_url": "https://www.dropbox.com/register",
        "signup_data": ""

    })
    if r.text[0:3] == "err":
        if r.text[6:11] == "email":
            return "email_error"
        elif r.text[6:11] == "funca":
            return "funcaptcha_error"
    else:
        return "success"


def main() -> bool:
    try:
        res = solver.funcaptcha(
            sitekey=SITE_KEY,
            url="https://www.dropbox.com/register"
        )
    except Exception as e:
        print(str(e))
        return False

    reg = register(res["code"])
    if reg == "funcaptcha_error":
        solver.report(res["captchaId"], False)
    else:
        solver.report(res["captchaId"], True)
    if reg == "email_error":
        return False
    return True


if __name__ == '__main__':
    main()
