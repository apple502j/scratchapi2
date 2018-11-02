# Checks if API is available. This file is in the public domain.
import sys
import requests
api = requests.get("https://api.scratch.mit.edu").status_code
if api>=400:
    print("API not available! Test failed.")
    sys.exit(1)
print("API confirmed.")
sys.exit(0)
