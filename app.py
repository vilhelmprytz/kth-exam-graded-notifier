#!/usr/bin/env python3

from os import environ
import requests
import time

TELEGRAM_API_TOKEN = environ["TELEGRAM_API_TOKEN"]
TELEGRAM_CHAT_ID = environ["TELEGRAM_CHAT_ID"]
KTH_COOKIE_AUTH = environ["KTH_COOKIE_AUTH"]


def send_to_telegram(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"

    try:
        response = requests.post(
            api_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message}
        )
    except Exception as e:
        print(e)


def get_exam_status():
    api_url = (
        "https://www.kth.se/student/minasidor/tentamen/api/visa-skannad-tenta/exams"
    )

    try:
        response = requests.get(
            api_url,
            cookies={"mod_auth_openidc_session": KTH_COOKIE_AUTH},
        )
        return response.json()
    except Exception as e:
        send_to_telegram(f"Error: {e}")
        print(e)


if __name__ == "__main__":
    send_to_telegram("Bot started")
    original_exams_arr = get_exam_status()

    while True:
        exams = get_exam_status()
        try:
            if exams != original_exams_arr:
                send_to_telegram("Tentan är rättad!")
                send_to_telegram("Tentan är rättad!")
                send_to_telegram("Tentan är rättad!")
                exit(1)
        except Exception as e:
            send_to_telegram(f"Error: {e}")
            print(e)

        time.sleep(60)
