import pyotp

totp = pyotp.TOTP("GBYHMZDVMVRVIV3YJ44G66LNPFRXG6LC")
print(totp.now())
