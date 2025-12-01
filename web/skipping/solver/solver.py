import os
import requests

url = "http://{}:{}/flag".format(os.getenv("CTF4B_HOST"), os.getenv("CTF4B_PORT"))

def solve(url):
    res = requests.get(url, headers={"x-ctf4b-request":"ctf4b"})
    return res.text

if __name__ == "__main__":
    flag = solve(url)
    print(flag)