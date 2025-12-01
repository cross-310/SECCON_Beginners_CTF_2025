# Writeup

ソースコードは以下.

```py
allowed_hostname = "example.com"
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)

# Remove port if present
input_hostname = None
if ':' in parsed.netloc:
    input_hostname = parsed.netloc.split(':')[0]

try:
    if parsed.hostname == allowed_hostname:
        print("You entered the allowed URL :)")
    elif input_hostname and input_hostname == allowed_hostname and parsed.hostname and parsed.hostname.startswith(allowed_hostname):
        print(f"Valid URL :)")
        print("Flag: ctf4b{dummy_flag}")
    else:
        print(f"Invalid URL x_x, expected hostname {allowed_hostname}, got {parsed.hostname if parsed.hostname else 'None'}")
except Exception as e:
    print("Error happened")
```


入力されたURLを受け取り, `urllib.parse`の`urlparse`でパースする.

```py
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)
```

netlocにportが含まれる場合にそれを除去する処理が入っている. `:`でsplitして先頭のものを検証に使用する.

```py
# Remove port if present
input_hostname = None
if ':' in parsed.netloc:
    input_hostname = parsed.netloc.split(':')[0]
```

`:`でnetlocをsplitした先頭のものが`example.com`, かつパースされたURLのhostnameの先頭が`example.com`である場合にflagが得られる. そのため, url-checkerと同じ解法(`//example.com.attacker.com`)では, 2つ目の条件しか満たせない.

```py
allowed_hostname = "example.com"
...
if parsed.hostname == allowed_hostname:
    print("You entered the allowed URL :)")
elif input_hostname and input_hostname == allowed_hostname and parsed.hostname and parsed.hostname.startswith(allowed_hostname):
    print(f"Valid URL :)")
    print("Flag: ctf4b{dummy_flag}")
```

1つ目の条件を満たすために, Basic認証の認証情報をURL内に格納する際に`:`を使用することを思い出す([参考](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Authentication#access_using_credentials_in_the_url)).

これを利用すると, `//example.com:pass@example.com.attacker.com`などで2つの条件を満たすことができる.

```
$ nc localhost 33458

 _   _ ____  _        ____ _               _             
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ __ 
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |   
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_|   

allowed_hostname = "example.com"                                                         
>> Enter a URL: //example.com:pass@example.com.attacker.com
Valid URL :)
Flag: ctf4b{cu570m_pr0c3551n6_0f_url5_15_d4n63r0u5}
```