1. `ps_shellcode_gen.ps1`でシェルコードをバイナリファイルとして保存する
2. 任意の逆アセンブラでソースコードを表示する（例：objdump -D -b binary -M addr64,data64 -m i386:x86-64）
3. `mov    %gs:0x60,%rax`でPEBのアドレスを求め、`0x20(%rax),%rax`でRTL\_USER\_PROCESS\_PARAMETERSのアドレスを求め、`mov    0x80(%rax),%rsi`で環境変数が格納されるアドレスを求めていることが分かる。
4. `CTF4B=1`という文字列と環境変数をcmpしていることが分かるため、環境変数`CTF4B`に`1`を設定すればフラグが表示されることが分かる。
