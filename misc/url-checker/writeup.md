# Writeup

ソースコードは以下.

```py
allowed_hostname = "example.com"
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)

try:
    if parsed.hostname == allowed_hostname:
        print("You entered the allowed URL :)")
    elif parsed.hostname and parsed.hostname.startswith(allowed_hostname):
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

パースされたURLのhostnameの先頭が`example.com`である場合にflagが得られる.

```py
allowed_hostname = "example.com"
...
if parsed.hostname == allowed_hostname:
    print("You entered the allowed URL :)")
elif parsed.hostname and parsed.hostname.startswith(allowed_hostname):
    print(f"Valid URL :)")
    print("Flag: ctf4b{dummy_flag}")
```

`//example.com.attacker.com`のようなURLを送信すればflagが得られる.

```
$ nc localhost 33457

 _   _ ____  _        ____ _               _             
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ __ 
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |   
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_|   

allowed_hostname = "example.com"                                                         
>> Enter a URL: //example.com.attacker.com
Valid URL :)
Flag: ctf4b{574r75w17h_50m371m35_n07_53cur37}
```