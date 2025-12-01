# TimeOfControl - SECCON Beginners CTF 2025

## 配布ファイルの説明

この問題の配布ファイルは、[こちらのリンク](https://file.beginners.seccon.jp/978122f78fd34a390efc3082dcd03fbeef7c91b4/TimeOfControl-112237ba07f4ed759f735da89c6d853e2fe9baad.zip)からダウウンロードしてください。
ダウンロードしたファイルを展開すると、次のようなファイルやフォルダがあります。

### src/ctf4b.{c,h}
今回の攻撃対象となるカーネルドライバのソースコードです。
このソースコードを読み、脆弱性を探してください。

### src/ctf4b.ko
実際のカーネルドライバをビルドしてできたEFLファイルです。

### src/rootfs.cpio
ディスクイメージです。initramfsとも呼ばれます。
実際の内容は、次のようなコマンドで./extへ展開することができます。
```sh
sudo rm -rf ./ext; mkdir ext; cd ext; sudo cpio -idv < ../rootfs.cpio; cd ../
```
extの中身を再度圧縮し、rootfs.cpioへ戻すには次のようなコマンドを利用します。
```sh
sudo find . -print0 | sudo cpio -o --format=newc --null > ../rootfs.cpio
```

### src/bzImage
Linuxの本体です。[extract-vmlinux](https://github.com/torvalds/linux/blob/master/scripts/extract-vmlinux)などのツールを用いることで、ELFファイルへと変換することができます。

### src/{Dockerfile,docker-compse.yml,run.sh}
これらのファイルは、サーバと同じ環境を手元に用意する際に必要です。
srcフォルダの中で次のコマンドを実行することで起動が可能です。
```sh
docker compose up --build -d
```
起動した環境へは、次のようにしてアクセスできます。
```sh
nc localhost 9004
```

### template/exploit.c
今回のカーネルモジュールを利用する方法を示したファイルです。
exploitを書く際のテンプレートとしてご利用ください。

### template/Makefile
exploitをビルドすることができます。
また、`make prepare`を行うことで、rootfs.cpioの/bin/の中へexploitをインストールすることができます。

### template/sender.py
作成したexploitをサーバへと送信し、それを実行するためのスクリプトです。
必要に応じてHOSTやPORTの値を調整してください。

## サーバへの接続方法について
リモートサーバでは、負荷低減のためにhashcashを用いたPoWの仕組みが導入されています。
sender.pyはそれらの処理を自動的に行うため、hashcashがインストールされていれば追加の作業は不要です。
一方で、sender.pyを利用しない場合、以下の方法でPoWを提示してください。

サーバへアクセスすると、次のような表示が出ます(実際の表示は毎回異なります)。
```txt
proof of work:
curl -sSfL https://pwn.red/pow | sh -s s.AAAu4A==.Iknt+X2n8KtNksUndKrxrg==
```
接続を続けるには、二行目の`curl -sSfL https:// ...`のコードをシェルで実行してください。
実行が終わると、文字列が表示されます。それをそのままサーバへ送信することで、PoWは完了です。
